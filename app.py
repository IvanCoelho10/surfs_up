# Import dependencies
from flask import Flask, request, redirect, jsonify
import numpy as np 
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
import pandas as pd

# SET UP FLASK APP

app = Flask(__name__)


# SET UP DATABASE & DB REFERENCES
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

# CREATE FLASK ROUTES
################################################################
@app.route("/")
# Home page.
# Lists all routes that are available...
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')


################################################################
@app.route("/api/v1.0/precipitation") 
# Convert the query results to a dictionary using `date` as the key and `prcp` as the value.
# Return the JSON representation of your dictionary.
def precipitation():
    # Connect to database
    session = Session(engine)

    # YOUR JOB: DEFINE THE precipitation_data VARIABLE
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
    
    # Disconnect from database
    session.close()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)
    


################################################################
@app.route("/api/v1.0/stations")
# Return a JSON list of stations from the dataset.
def stations():
    # Connect to database
    session = Session(engine)

    # YOUR JOB: DEFINE THE stations_list VARIABLE
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    # Disconnect from database
    session.close()
    return jsonify(stations=stations)
    #return jsonify(stations)


################################################################
@app.route("/api/v1.0/tobs")
# Query the dates and temperature observations of the most active station for the last year of data.
# Return a JSON list of temperature observations (TOBS) for the previous year.
#def tobs():
def temp_monthly():
    # Connect to database
    session = Session(engine)
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    # Disconnect from database
    session.close()
    #return jsonify(tobs)
    return jsonify(temps=temps)


################################################################
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
# When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.
def stats(start=None, end=None):
    
    # Connect to database
    session = Session(engine)

    # YOUR JOB: DEFINE THE temps_filtered_by_date VARIABLE
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps=temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    
    # Disconnect from database
    session.close()
    #return jsonify(temps_filtered_by_date)
    return jsonify(temps)
# Run the Flask app that was created at the top of this file --> app = Flask(__name__)
################################################################
if __name__ == '__main__':
    app.run(debug=True) # set to false if deploying to a live website server (such as Google Cloud, Heroku, or AWS Elastic Beanstaulk)