# Import the dependencies.
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


#################################################
# Flask Routes
#################################################
@app.route("/api/v1.0/precipitation")
def precipitation():
    date2 = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    prcp=[]
    prcp = session.query(measurement.date,measurement.prcp).all()
    prcp = session.query(measurement.date, measurement.prcp).filter(measurement.date >= date2).all()
    precipitation = {date:prcp for date,prcp in prcp}
    return jsonify(precipitation)
@app.route("/api/v1.0/stations")
def stations():
    station1 = []
    station1 = session.query(station.station).all()
    station1 = list(np.ravel(station1))
    return jsonify(station1)
@app.route("/api/v1.0/tobs")
def tobs():
    date2 = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    x = session.query(measurement.station, func.count(measurement.station)).\
group_by(measurement.station).order_by(func.count(measurement.station).desc()).all()
    temp = session.query(measurement.date, measurement.tobs).filter(measurement.station == x[0].station).\
filter(measurement.date >= date2).all()
    temp = list(np.ravel(temp))
    return jsonify(temp)


if __name__ == '__main__':
    app.run(debug=True)
