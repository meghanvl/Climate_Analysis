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

#1. Convert the query results to a dictionary using date as the key and prcp as the value. 
#Return the JSON representation of your dictionary.

@app.route("/api/v1.0/precipitation")
def precipitation():
    
    session = Session(engine)
    
    results = session.query(Measurement.date, Measurement.prcp).all()
    
    session.close()
    
    precipitation = []
    for row in results:
        precip_dict = {}
        precip_dict["date"] = row.date
        precip_dict["prcp"] = row.prcp
        precipitation.append(precip_dict)

    return jsonify(precipitation)

#2. Return a JSON list of stations from the dataset.

@app.route("/api/v1.0/stations")
def stations():
    
    session = Session(engine)
    
    results = session.query(Station.name).all()
    
    all_names = list(np.ravel(results))

    return jsonify(all_names)

#3. Query the dates and temperature observations of the most active station for the last year of data.
#Return a JSON list of temperature observations (TOBS) for the previous year.

@app.route("/api/v1.0/tobs")
def tobs():
    
    session = Session(engine)
    
    #last date
    last_date = session.query(Measurement.date).\
            order_by(Measurement.date.desc()).\
            first().date
    
    #date from one year ago
    last_twelve = dt.datetime.strptime(last_date, '%Y-%m-%d') - dt.timedelta(days=366)
    
    #retrieve station names and count descending
    results = (session.query(Measurement.station, func.count(Measurement.station)).\
                   group_by(Measurement.station).\
                   order_by(func.count(Measurement.station).desc()).\
                   all())
    
    most_active = results[0][0]
    print(most_active)
    
    #last year of data for most active station
    station_one_year = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
            filter(Measurement.date > last_twelve).\
            filter(Measurement.station == most_active).\
            group_by(Measurement.date).all()
   

    return jsonify(station_one_year)







if __name__ == "__main__":
    app.run(debug=True)