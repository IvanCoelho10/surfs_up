# Import dependencies
from flask import Flask, request, redirect, jsonify
import numpy as np 
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


# SET UP FLASK APP
app = Flask(__name__)


# SET UP DATABASE & DB REFERENCES
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station


# CREATE FLASK ROUTES
################################################################
@app.route("/")
# Home page.
# Lists all routes that are available...
def home():
    homepageHTML = (
        f"<h1>Welcome to the Hawaii Climate Analysis API!</h1>"
        f"<h2>Available API Endpoints:</h2><br/>"

        f"<h3>🌧 PRECIPITATION:</h3>"
        f"<a href='/api/v1.0/precipitation'>/api/v1.0/precipitation</a><br/><br/><br/><br/>"

        f"<h3>📡 STATIONS:</h3>"
        f"<a href='/api/v1.0/stations'>/api/v1.0/stations</a><br/><br/><br/><br/>"
        
        f"<h3>🌡 TEMPERATURE OBSERVATIONS:</h3>"
        f"<a href='/api/v1.0/tobs'>/api/v1.0/tobs</a><br/><br/><br/><br/>"

        f"<h3>📆 SPECIFIED START DATE:</h3>"
        f"/api/v1.0/temp/YYYY-MM-DD<br/><br/><br/><br/>"

        f"<h3>📆 SPECIFIED START DATE & END DATE:</h3>"
        f"/api/v1.0/temp/YYYY-MM-DD/YYYY-MM-DD"
    )
    return homepageHTML


################################################################
@app.route("/api/v1.0/precipitation") 
# Convert the query results to a dictionary using `date` as the key and `prcp` as the value.
# Return the JSON representation of your dictionary.
def precipitation():
    # Connect to database
    session = Session(engine)

    # YOUR JOB: DEFINE THE precipitation_data VARIABLE

    # Disconnect from database
    session.close()
    return jsonify(precipitation_data)


################################################################
@app.route("/api/v1.0/stations")
# Return a JSON list of stations from the dataset.
def stations():
    # Connect to database
    session = Session(engine)

    # YOUR JOB: DEFINE THE stations_list VARIABLE

    # Disconnect from database
    session.close()
    return jsonify(stations_list)


################################################################
@app.route("/api/v1.0/tobs")
# Query the dates and temperature observations of the most active station for the last year of data.
# Return a JSON list of temperature observations (TOBS) for the previous year.
def tobs():
    # Connect to database
    session = Session(engine)

    # YOUR JOB: DEFINE THE tobs_data VARIABLE

    # Disconnect from database
    session.close()
    return jsonify(tobs_data)


################################################################
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
# When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.
def start_and_end(start='YYYY-MM-DD', end='YYYY-MM-DD'):
    
    # Connect to database
    session = Session(engine)

    # YOUR JOB: DEFINE THE temps_filtered_by_date VARIABLE

    # Disconnect from database
    session.close()
    return jsonify(temps_filtered_by_date)

# Run the Flask app that was created at the top of this file --> app = Flask(__name__)
################################################################
if __name__ == '__main__':
    app.run(debug=True) # set to false if deploying to a live website server (such as Google Cloud, Heroku, or AWS Elastic Beanstaulk)