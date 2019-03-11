# 1. import Flask
from flask import Flask

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

# 3. Define what to do when a user hits the index route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Calculate the date 1 year ago from the last data point in the database
    year =  dt.timedelta(days=365)
    year_prior = dt.datetime.strptime(last_data,'%Y-%m-%d') - year

    # Perform a query to retrieve the date and precipitation scores
    precip_date = session.query(Measurement.date).filter(Measurement.date > year_prior).all()
    precip = session.query(Measurement.prcp).filter(Measurement.date > year_prior).all()

    # List comprehension
    precip_date_list = list(np.ravel(precip_date))
    # print(len(precip_date_list))
    # print(precip_date_list)

    precip_list = list(np.ravel(precip))
    # print(len(precip_list))
    # print(precip_list)

    # Save the query results as a Pandas DataFrame and set the index to the date column
    precip_data = {precip_date_list: precip_list}   
    
    # JSONify 
    return jsonify(precip_data)

# 4. Define what to do when a user hits the /about route
@app.route("/about")
def about():
    print("Server received request for 'About' page...")
    return "Welcome to my 'About' page!"


if __name__ == "__main__":
    app.run(debug=True)
