import datatime as dt
import numpy as np 
import pandas as pd 
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, render_template


engine = create_engine("sqlite:///hawaii.sqlite")



base = automap_base()

Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

session =Session(engine)

app = Flask(__name__)


@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii Climate Analysis API!<br>"
        f"Available Routes: <br>"
        f"/api/v1.0/precipitation <br>"
        f"/api/v1.0/stations <br>"
        f"/api/v1.0/tobs <br>"
        f"/api/v1.0/temp/start/end <br>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    prev_yr = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    precipitation= session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_yr).all()

    precip = {date: prcp for date, prcp in precipitation}

    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    
    results= session.query(Station.station).all()

    stations = list(np.ravel(results))

    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def temp_monthly():
    
    prev_yr = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results= session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_yr).all()

    tenps = list(np.ravel(results))

    return jsonify(tenps)


@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):

sel = [func.min(Measurement.tobs),func.avg(Measurement.tobs), func.max(Measurement.tobs)]    
If not end:
    
    results= session.query(*sel).\
        filter(Measurement.date >= start).all()

    tenps = list(np.ravel(results))

    return jsonify(tenps)

results= session.query(*sel).\
    filter(Measurement.date >= start).\
    filter(Measurement.date >= end).all()

tenps = list(np.ravel(results))

return jsonify(tenps)

if __name__ == "__main__":
    app.run(port= 8000, debug=True)
