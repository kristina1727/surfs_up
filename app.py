# Import dependencies
import datetime as dt
from re import M
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from flask import Flask, jsonify
from sqlalchemy.sql.traversals import TraversalComparatorStrategy

# Set up the database
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect the database into our classes
Base = automap_base()
Base.prepare(engine,reflect = True)

#print(Base.classes.keys())
# inspector = inspect (engine)
# columns = inspector.get_columns('measurement')
# print (columns)
# save our references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# create a session link from Python to our database
session = Session(engine)

# Define the app for the flask applicaiton
app = Flask(__name__)

# create our first route
@app.route('/')

# Create  function called welcome
def welcome():
    return(
        '''
        Welcome to the Climate Analysis API!
        <br>Available Routes:
        <br>/api/v1.0/precipitation
        <br>/api/v1.0/stations
        <br>/api/v1.0/tobs
        <br>/api/v1.0/temp/start/end
        ''')

# Create precipitiaion analysis route
@app.route("/api/v1.0/precipitation")

# Create the precipitation function
def precipitation():
    prev_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return(jsonify(precip))

# Create station route
@app.route("/api/v1.0/stations")

# Create the precipitation function
def stations():
    results = session.query(Station.station).all()
    # unravel results into a one-dimensional array
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# Create tobs route
@app.route("/api/v1.0/tobs")

# Create the temp monthly function
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# Create the start/end route
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

# Create the stats function
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)