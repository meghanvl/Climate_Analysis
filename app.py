import numpy as np
import sqlalchemy
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
    return f"Available Routes:"
            "/api/v1.0/precipitation"
            "/api/v1.0/stations"
            "/api/v1.0/tobs"
            "/api/v1.0/<start>"
            "/api/v1.0/<start>/<end>"