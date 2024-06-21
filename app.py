import click
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint
from .ingest import generate_statistics, ingest_wx_data

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://postgres:password@db:5432/weather_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Todo List API"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

db = SQLAlchemy(app)

class WeatherRecord(db.Model):
    """
    Represents a weather record in the database.
    """
    id = db.Column(db.Integer, primary_key=True)
    station = db.Column(db.String(15))
    date = db.Column(db.String(8))
    maximum_temperature = db.Column(db.Integer)
    minimum_temperature = db.Column(db.Integer)
    precipitation = db.Column(db.Integer)

    @property
    def serialize(self):
        """
        Serialize the weather record to a dictionary format.
        """
        return {
            "station": self.station,
            "date": self.date,
            "maximum_temperature": self.maximum_temperature,
            "minimum_temperature": self.minimum_temperature,
            "precipitation": self.precipitation,
        }

class Statistic(db.Model):
    """
    Represents statistical data for weather records in the database.
    """
    id = db.Column(db.Integer, primary_key=True)
    station = db.Column(db.String(15))
    date = db.Column(db.String(8))
    final_maximum_temperature = db.Column(db.Integer)
    final_minimum_temperature = db.Column(db.Integer)
    final_precipitation = db.Column(db.Integer)

    @property
    def serialize(self):
        """
        Serialize the statistic record to a dictionary format.
        """
        return {
            "station": self.station,
            "date": self.date,
            "final_maximum_temperature": self.final_maximum_temperature,
            "final_minimum_temperature": self.final_minimum_temperature,
            "final_precipitation": self.final_precipitation,
        }

@click.command(name="create")
def create():
    """
    CLI command to create the database tables and ingest initial data.
    """
    with app.app_context():
        db.drop_all()
        db.create_all()
        ingest_wx_data()
        generate_statistics()

@app.route("/api/weather/", methods=["GET"])
def weather_home():
    """
    API endpoint to retrieve weather records with optional filtering by date and station.
    """
    page = request.args.get("page", 1, type=int)
    date = request.args.get("date")
    station = request.args.get("station")
    result = WeatherRecord.query
    if date:
        result = result.filter(WeatherRecord.date == date)
    if station:
        result = result.filter(WeatherRecord.station == station)

    records = result.paginate(page=page, per_page=100, error_out=False).items
    return jsonify([r.serialize for r in records])

@app.route("/api/weather/stats/", methods=["GET"])
def stats():
    """
    API endpoint to retrieve statistical weather data with optional filtering by date and station.
    """
    page = request.args.get("page", 1, type=int)
    date = request.args.get("date")
    station = request.args.get("station")
    result = Statistic.query
    if date:
        result = result.filter(Statistic.date == date)
    if station:
        result = result.filter(Statistic.station == station)

    records = result.paginate(page=page, per_page=100, error_out=False).items
    return jsonify([r.serialize for r in records])

app.cli.add_command(create)

if __name__ == "__main__":
    app.run(debug=True)
