import pytest
from .app import app

@pytest.fixture
def client():
    """
    Sets up the testing client for the Flask application and initializes the database with test data.
    
    Yields:
        FlaskClient: The testing client for the Flask application.
    """
    from .app import db, WeatherRecord, Statistic
    app.config["TESTING"] = True
    with app.app_context():
        db.drop_all()
        db.create_all()
        
        weather_data = [
            WeatherRecord(
                station="station1",
                date="19850101",
                maximum_temperature=1,
                minimum_temperature=1,
                precipitation=10,
            ),
            WeatherRecord(
                station="station2",
                date="19860101",
                maximum_temperature=2,
                minimum_temperature=2,
                precipitation=20,
            ),
            WeatherRecord(
                station="station1",
                date="19860101",
                maximum_temperature=3,
                minimum_temperature=3,
                precipitation=30,
            ),
        ]
        db.session.bulk_save_objects(weather_data)
        
        stats_data = [
            Statistic(
                station="station1",
                date="1985",
                final_maximum_temperature=1,
                final_minimum_temperature=1,
                final_precipitation=10,
            ),
            Statistic(
                station="station2",
                date="1986",
                final_maximum_temperature=2,
                final_minimum_temperature=2,
                final_precipitation=20,
            ),
        ]
        db.session.bulk_save_objects(stats_data)
        db.session.commit()

    with app.test_client() as client:
        yield client

def test_weather_reports(client):
    """
    Tests the /api/weather/ endpoint to ensure it returns the correct number of weather records.
    """
    response = client.get("/api/weather/")
    assert response.status_code == 200
    assert len(response.json) == 3

def test_weather_reports_filter_by_date(client):
    """
    Tests the /api/weather/ endpoint with a date filter to ensure it returns the correct records.
    """
    response = client.get("/api/weather/?date=19860101")
    assert response.status_code == 200
    assert len(response.json) == 2

def test_weather_reports_filter_by_station(client):
    """
    Tests the /api/weather/ endpoint with a station filter to ensure it returns the correct records.
    """
    response = client.get("/api/weather/?station=station1")
    assert response.status_code == 200
    assert len(response.json) == 2

def test_weather_reports_filter_by_station_and_date(client):
    """
    Tests the /api/weather/ endpoint with both station and date filters to ensure it returns the correct record.
    """
    response = client.get("/api/weather/?station=station1&date=19860101")
    assert response.status_code == 200
    assert len(response.json) == 1

def test_weather_reports_pagination(client):
    """
    Tests the /api/weather/ endpoint with pagination to ensure it returns the correct records for each page.
    """
    response = client.get("/api/weather/?page=1")
    assert response.status_code == 200
    assert len(response.json) == 3

    response = client.get("/api/weather/?page=2")
    assert response.status_code == 200
    assert len(response.json) == 0

def test_stats(client):
    """
    Tests the /api/weather/stats/ endpoint to ensure it returns the correct number of statistical records.
    """
    response = client.get("/api/weather/stats/")
    assert response.status_code == 200
    assert len(response.json) == 2

def test_stats_filter_by_date(client):
    """
    Tests the /api/weather/stats/ endpoint with a date filter to ensure it returns the correct records.
    """
    response = client.get("/api/weather/stats/?date=1986")
    assert response.status_code == 200
    assert len(response.json) == 1

def test_stats_filter_by_station(client):
    """
    Tests the /api/weather/stats/ endpoint with a station filter to ensure it returns the correct records.
    """
    response = client.get("/api/weather/stats/?station=station1")
    assert response.status_code == 200
    assert len(response.json) == 1

def test_stats_filter_by_station_and_date(client):
    """
    Tests the /api/weather/stats/ endpoint with both station and date filters to ensure it returns the correct record.
    """
    response = client.get("/api/weather/stats/?station=station2&date=1986")
    assert response.status_code == 200
    assert len(response.json) == 1
