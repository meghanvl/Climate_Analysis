import numpy as np
import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Station = Base.classes.station
Measurement = Base.classes.measurement

app = Flask(__name__)


#1.List all routes that are available.

@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

#2. Convert the query results to a dictionary using date as the key and prcp as the value. 
#Return the JSON representation of your dictionary.

@app.route("/api/v1.0/precipitation")
def precipitation():
    
    session = Session(engine)
   
    
    #retrieve date and prcp data and display in dictionary
    results = session.query(Measurement.date, Measurement.prcp).all()
    
    session.close()
    
    precipitation = []
    for row in results:
        precip_dict = {}
        precip_dict["Date"] = row.date
        precip_dict["Precipiation"] = row.prcp
        precipitation.append(precip_dict)

    return jsonify(precipitation)

#3. Return a JSON list of stations from the dataset.

@app.route("/api/v1.0/stations")
def stations():
    
    session = Session(engine)
    
    #retrieve station information and display as dictionary
    results = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()
    
    session.close()
    
    name = []
    for row in results:
        name_dict = {}
        name_dict["Station"] = row.station
        name_dict["Name"] = row.name
        name_dict["Latitude"] = row.latitude
        name_dict["Longitude"] = row.longitude
        name_dict["Elevation"] = row.elevation
        name.append(name_dict)

    return jsonify(name)

#4. Query the dates and temperature observations of the most active station for the last year of data.
#Return a JSON list of temperature observations (TOBS) for the previous year.

@app.route("/api/v1.0/tobs")
def tobs():
    
    session = Session(engine)
    
    #last date
    last_date = session.query(Measurement.date).\
            order_by(Measurement.date.desc()).\
            first().date
    
    #date from one year ago
    last_twelve = dt.datetime.strptime(last_date, "%Y-%m-%d") - dt.timedelta(days=366)
    
    #retrieve station names and count descending
    results = (session.query(Measurement.station, func.count(Measurement.station)).\
                   group_by(Measurement.station).\
                   order_by(func.count(Measurement.station).desc()).\
                   all())
    
    session.close()
    
    most_active = results[0][0]
    print(most_active)
    
    #last year of data for most active station
    station_one_year = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
            filter(Measurement.date > last_twelve).\
            filter(Measurement.station == most_active).\
            group_by(Measurement.date).all()
    
    station_data = []
    for row in station_one_year:
        station_dict = {}
        station_dict["Station"] = row.station
        station_dict["Date"] = row.date
        station_dict["Temperature"] = row.tobs
        station_data.append(station_dict)
  

    return jsonify(station_data)


#5. Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
#When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
#When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.

@app.route("/api/v1.0/<start>")
def start(start):
    
    session = Session(engine)
    
    #date user enters
    start_date = dt.datetime.strptime(start, "%Y-%m-%d")
    
    calculations = session.query(func.min(Measurement.tobs), func.round(func.avg(Measurement.tobs)), func.max(Measurement.tobs)).\
                  filter(Measurement.date >= start_date).all()
    
    session.close()
    
    #append calculations to a list and display
    cal_list = []
    for row in calculations:
        start_dict = {"Date": start}
        cal_list.append(start_dict)
        cal_list.append({"Minimum Temperature": calculations[0][0]})
        cal_list.append({"Average Temperature": calculations[0][1]})
        cal_list.append({"Maximum Temperature": calculations[0][2]})
                                 
    
    return jsonify(cal_list)


#6.Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
#When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
#When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    
    session = Session(engine)
    
    #date user enters
    start_date = dt.datetime.strptime(start, "%Y-%m-%d")
    end_date = dt.datetime.strptime(end, "%Y-%m-%d")
    
    calculations = session.query(func.min(Measurement.tobs), func.round(func.avg(Measurement.tobs)), func.max(Measurement.tobs)).\
                  filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
                    
    
    session.close()
    
    
    #append calculations to a list and display
    cal_list = []
    for row in calculations:
        date_dict = {"Start Date": start, "End Date": end}
        cal_list.append(date_dict)
        cal_list.append({"Minimum Temperature": calculations[0][0]})
        cal_list.append({"Average Temperature": calculations[0][1]})
        cal_list.append({"Maximum Temperature": calculations[0][2]})
                                 
                   
    return jsonify(cal_list)
   
    
   
if __name__ == "__main__":
    app.run(debug=True)