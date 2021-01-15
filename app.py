from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return f"Available Routes:"

@app.route("/api/v1.0/precipitation")




@app.route("/api/v1.0/stations")




@app.route("/api/v1.0/tobs")




@app.route("/api/v1.0/<start>")



@app.route("/api/v1.0/<start>/<end>")