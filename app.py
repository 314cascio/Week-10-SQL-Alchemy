# 1. import Flask
from flask import Flask, jsonify

# 2. Create an app, being sure to pass __name__
app = Flask(__name__)

# import libraries
import numpy as np
import pandas as pd
import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func


engine = create_engine("sqlite:///02-Homework_10-SQL-Alchemy_Resources_hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# We can view all of the classes that automap found
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

 # Create our session (link) from Python to the DB
 session = Session(engine)

# Define precipitation route
@app.route("/api/v1.0/")
def index():
    return "Welcome to the Climate App"

    # List links
    return (
        f"Available Routes:</api/v1.0/precipitation>"
        f"</api/v1.0/stations>"
        f"</api/v1.0/tobs>")

# Define precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Perform a query to retrieve the date and precipitation scores
    precip_date = session.query(Measurement.date).all()
    precip = session.query(Measurement.prcp).all()

    # List comprehension
    precip_date_list = list(np.ravel(precip_date))
    precip_list = list(np.ravel(precip))

    # Save the list as a dictionary w/ Date as key and Precipitation as value
    precip_data = dict(zip(precip_date_list, precip_list))
    
    # JSONify 
    return jsonify(precip_data)

# Define stations route
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DBsession = Session(engine)
    station = session.query(Station.station).all()
    
    # Make list
    station_list = list(np.ravel(station))
    return jsonify(station_list)


# Define tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
   
    # Find the last data point
    last_data = session.query(func.max(Measurement.date)).scalar()

    # Calculate the date 1 year ago from the last data point in the database
    year =  dt.timedelta(days=365)
    year_prior = dt.datetime.strptime(last_data,'%Y-%m-%d') - year

    # Perform a query to retrieve the date and precipitation scores
    precip_date = session.query(Measurement.date).filter(Measurement.date > year_prior).all()
    precip = session.query(Measurement.prcp).filter(Measurement.date > year_prior).all()

    # List comprehension
    precip_date_list = list(np.ravel(precip_date))
    precip_list = list(np.ravel(precip))
 
    precip_data = dict(zip(precip_date_list, precip_list))
    return jsonify(precip_data)

# # Define tobs route
# @app.route("/api/v1.0/start")
# def start():
#     # Create our session (link) from Python to the DB
#     session = Session(engine)
    
#     # When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
#     start = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Station.date >= '2017-06-17').all()
   
#     # List comprehension
#     start_list = list(np.ravel(start))

#     return jsonify(start_list)



# # Define tobs route
# @app.route("/api/v1.0/trip")
# def trip():
#     # Create our session (link) from Python to the DB
#     session = Session(engine)

#     # When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
#     session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter((Station.date >= '2017-06-17') and (Station.date <= '2017-07-02')).all()
    
#     # Dates of my trip
#     start_date = '2017-06-17'
#     end_date = '2017-07-02'

#     # Use your previous function `calc_temps` to calculate the tmin, tavg, and tmax 
#     # for your trip using the previous year's data for those same dates.
#     calc_temps_list = calc_temps(start_date, end_date)
    
#     # List comprehension
#     start_list = list(np.ravel(calc_temps_list))
   
#     # Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
#     return jsonify(calc_temps_list)


if __name__ == "__main__":
    app.run(debug=True)
