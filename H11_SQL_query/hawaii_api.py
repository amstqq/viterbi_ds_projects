
# coding: utf-8

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy import create_engine, func
import datetime as dt


from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Calculate the date 1 year ago from today
    last_year = dt.datetime.now() - dt.timedelta(days=2*365)
    # Perform a query to retrieve the data and precipitation scores
    results = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date>last_year).all()

    # Create a dictionary from the row data and append to a list
    last_year_prcp = []
    for result in results:
        prcp_dict = {}
        prcp_dict['date'] = result.date
        prcp_dict['prcp'] = result.prcp
        last_year_prcp.append(prcp_dict)

    return jsonify(last_year_prcp)

@app.route("/api/v1.0/stations")
def stations():
    # Query all stations
    results = session.query(Station.station).all()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    last_year = dt.datetime.now() - dt.timedelta(days=2*365)
    # Query all tobs
    results = session.query(Measurement.tobs).filter(Measurement.date>last_year).all()
    # Convert list of tuples into normal list
    all_tobs = list(np.ravel(results))

    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>/")
@app.route("/api/v1.0/<start>/<end>")
# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
def temperature(start, end = None):
    if start <= '2017-08-23':
        if end == None:
            """ calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date."""
            results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                        filter(Measurement.date >= start).all()
            temp_dict = {}
            temp_dict['TMIN'] = results[0][0]
            temp_dict['TAVG'] = results[0][1]
            temp_dict['TMAX'] = results[0][2]

            return jsonify(temp_dict)
        elif end > start:
            results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
            temp_dict = {}
            temp_dict['TMIN'] = results[0][0]
            temp_dict['TAVG'] = results[0][1]
            temp_dict['TMAX'] = results[0][2]

            return jsonify(temp_dict)

    return jsonify({"error": f"Precipitation data with start date {start} and end date {end} not found."}), 404

if __name__ == '__main__':
    app.run(debug=True)
