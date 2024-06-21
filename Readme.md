# Weather API
We are provided with dataset folder containing the weather history of different location at different period of time. This project demonstrate the use case of flask framework with large data ingestion in Postgres DB. The project is also fully dockerised. The APIs created allows you to access weather data for various locations and years. The data can be filtered by date and location. The API also provides statistical information on the weather data.

# Pre-Requisites

To run this application make sure your machine has pre-installed:
- Docker 
- Python

# Folder Structure
```
.
├── data                   
    ├── wx_data
    ├── yld_data
    
├── logs                    
├── static                 
├── __init__.py             
├── .coveragerc
├── .gitignore
├── app.py             
├── docker-compose.yml
├── dockerfile
├── ingest.py
├── README.md
├── requirements.txt
└── test_api.py          
```


# Set-Up

- Start Docker and run the following command:
```bash
docker-compose up -d --build
```

- Ingest the give data:

```bash
docker-compose exec web flask create
```

- The API can now be accessed at http://localhost:5003.

## **Swagger**
You can access all the end-points using Swagger at
[http://localhost:5003/swagger/](http://localhost:5003/swagger/)

#### Weather data
- This endpoint returns a paginated list of weather records:
```
GET /api/weather/
```

![](/static/get-weather.png)

- You can use `page` query parameter to get a particular page.
```
GET /api/weather/?page=1
```
![](/static/get-weather-page.png)
- You can filter the results by date and station using `date` and `station` query parameters.
```
GET /api/weather/?date=19850103&station=USC00257715
```
![](/static/get-weather-filter.png)

#### Statistics
- This endpoint returns statistical information about the weather data.
```
GET /api/weather/stats/
```
![](/static/get-weather-stat.png)

- You can use `page` query parameter to get a particular page.
```
GET /api/weather/stats/?page=1
```
![](/static/get-weather-stat-page.png)
- You can filter the results by date and station using `date` and `station` query parameters.
```
GET /api/weather/stats/?date=19850103&station=USC00257715
```

## Testing
For testing the application is leveraging Pytest. You can run test using:
```bash
docker-compose exec web pytest
```
The test coverage is 99%

![](/static/test-coverage.png)