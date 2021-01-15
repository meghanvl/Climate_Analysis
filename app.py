from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return f"Available Routes:"
            "/api/v1.0/precipitation"
            "/api/v1.0/stations"
            "/api/v1.0/tobs"
            "/api/v1.0/<start>"
            "/api/v1.0/<start>/<end>"