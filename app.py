# Import dependencies
import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from flask import Flask, jsonify

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
        Available Routes:
        /api/v1.0/precipitation
        /api/v1.0/stations
        /api/v1.0/tobs
        /api/1.0/temp/start/end
        ''')

# Create precipitiaion analysis route
@app.route("/api/v1.0/precipitation")
