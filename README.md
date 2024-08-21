# weatherAPI
Weather API

# About

REST API which connects to [OpenWeather APIs](https://openweathermap.org/api) to return information about weather on a given date and in a given location.
This API makes use of a local SQLite database to cache results to reduce the number of calls to [OpenWeather APIs](https://openweathermap.org/api).

When a request is made to this API, the sequence of events is as follows

1) The local database is checked for cached results relating to this request. If a result is found, the database record is returned.

2) If a database record is not found, a request is made to the [OpenWeather GeoCoding API](https://openweathermap.org/api/geocoding-api). This uses the name given and returns the latitude and longitude values for that city.

3) The latitude, logitude, and date and used to make a request to the [OpenWeather Daity Aggregation API](https://openweathermap.org/api/one-call-3#history_daily_aggregation).

4) The maximum temperature, minimum temperature, and humidity values are extracted from the response. Then the information is written to the database. Finally, the average temperature is calculated.

5) These values are returned to the user.

Each time a request is made to the [OpenWeather APIs](https://openweathermap.org/api), the response code is checked and in the case of an error, an appropriate message is returned to the user.

### Requirements:
    - pip3 install requests
    - pip3 install statistics
    - pip3 install "fastapi[standard]"

    SQLite is included in MacOS, it will need to be installed in Windows.

## Getting Started

This can be run both locally and in a docker container.
All required files are provided.

### Prerequisites

Requirements for the software and other tools to build, test and push 
- Python version >= 3.9
- requests module
- statistics module
- fastAPI

SQLite is used but is included by default in MacOS.

### Installing

To run locally:

Open a Terminal window and navigate to the weatherAPI folder

Create a virutal environment

    python3 -m venv .venv

Activate the virtual environment

    source .venv/bin/activate

Install requirements

    pip3 install requests
    pip3 install statistics
    pip3 install "fastapi[standard]"

To start the API locally

    fastapi dev main.py

By default, the API will be available at http://127.0.01:8000. Browsing to this address will display a basic output.

## Usage

The API can be accessed at the endpoint http://127.0.0.1:8000/get-weather?{CITY}=London&date={DATE}
Where {CITY} is the name of the city and {DATE} is the date in the format YYYY-MM-DD

The API will return information in teh following format:

    {
    "minTemp": float,
    "maxTemp": float,
    "avgTemp": float,
    "humidity": float
    }

More information about the API endpoints can be found at http://127.0.0.1:8000/docs

## Running the tests

Unit testing makes use of PyTest.

The unit tests are found in the test_resources.py file and contain test cases for functions in the resources.py file.

There is also an API test. This test contains a set of known historical data from the [OpenWeather Daity Aggregation API](https://openweathermap.org/api/one-call-3#history_daily_aggregation). The test makes a request to this APU and compares the results to the know expected data.

### Sample Tests

Example of a unit test

    def test_calculate_avg_temp():
        # Test the calculate avg temp function
        assert resources.calculate_avg_temp(10, 20) == 15
        assert resources.calculate_avg_temp(10, 20) != 10
        assert resources.calculate_avg_temp(50, 30) == 40
        assert resources.calculate_avg_temp(10, 20) != 100

## Authors

  - **Peter Hudson**
    [LinkedIn](www.linkedin.com/in/peter-t-hudson)
    [GitHub](https://github.com/peterthudson)

