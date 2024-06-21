import datetime
import os
import logging
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text

logging.basicConfig(filename="logs/record.log", level=logging.DEBUG)
logger = logging.getLogger(__name__)

def read_wx_data():
    """
    Reads weather data from text files in the 'data/wx_data' directory.
    
    Returns:
        list: A list of WeatherRecord objects containing the parsed weather data.
    """
    logger.info("Reading wx Data...")
    weather = []
    path = os.path.join(os.getcwd(), "data/wx_data")
    from .app import WeatherRecord
    for file in os.listdir(path):
        if file.endswith(".txt"):
            logger.info(f"Reading file: {file}")
            fpath = os.path.join(path, file)
            with open(fpath, "r") as data:
                lines = [line.rstrip() for line in data]
                for line in lines:
                    temp = line.split("\t")
                    w = WeatherRecord(
                        station=file[:-4],
                        date=int(temp[0]),
                        maximum_temperature=int(temp[1]),
                        minimum_temperature=int(temp[2]),
                        precipitation=int(temp[3]),
                    )
                    weather.append(w)

    logger.info(f"Weather File read complete: found {len(weather)} records")
    return weather

def ingest_wx_data():
    """
    Ingests weather data into the database by reading it from text files and saving it in bulk.
    """
    from .app import db
    initial_time = datetime.datetime.now()

    try:
        weather = read_wx_data()
        db.session.bulk_save_objects(weather)
        db.session.commit()
        logger.info("Weather data loaded successfully.")
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Error inserting weather data: {e}")
    finally:
        completion_time = datetime.datetime.now()
        logger.info(f"Weather Data inserted in : {(completion_time-initial_time).total_seconds()} secs. Total rows: {len(weather)}")

def generate_statistics():
    """
    Generates statistical data from the weather records and inserts it into the 'statistic' table.
    """
    from .app import db
    query = """
    INSERT INTO statistic(station, date, final_maximum_temperature, final_minimum_temperature, final_precipitation)
    SELECT station, SUBSTRING(date, 1, 4) as date, AVG(maximum_temperature), AVG(minimum_temperature), SUM(precipitation)
    FROM weather_record
    WHERE maximum_temperature != -9999
      AND minimum_temperature != -9999
      AND precipitation != -9999
    GROUP BY station, date
    """

    try:
        db.session.execute(text(query))
        db.session.commit()
        logger.info("Statistics data loaded successfully.")
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Error generating statistics: {e}")
