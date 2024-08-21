from fastapi import FastAPI
import requests
import resources
import sqlite3

app = FastAPI()

# Set up the SQLite database
con = sqlite3.connect('weather.db', check_same_thread=False)
cur = con.cursor()
if not resources.db_confirm_database_exists(cur):
    print("Failed to set up database")
else:
    print("Local database set up")

# Create the required weather table with columns for city name, date, max temp, min temp, and humidity.
# Average temp will not be stored as it is caluclated from values in the table
cur.execute("CREATE TABLE if not exists weather(city_name, date, max_temp, min_temp, humidity)")
con.commit()

# Routes
@app.get("/")
def root():
    return {"message": "Weather API"}

@app.get("/get-weather")
def get_weather(city: str, date: str):

    # Check that there is an entry in the database for this city and date.
    # If there is, query it and return those results
    if resources.db_check_record_exists(con, city, date):

        resultsDict = {
            "min" : float(resources.db_return_row(con, city, date)[3]),
            "max" : float(resources.db_return_row(con, city, date)[2]),
            "avg" : resources.calculate_avg_temp(resources.db_return_row(con, city, date)[3], resources.db_return_row(con, city, date)[2]),
            "hum" : float(resources.db_return_row(con, city, date)[4])
        }
        return resultsDict
    
    # If there isn't, get the data and create a database entry
    
    # get data from GeoCoding API
    geoResponse = requests.get(resources.openWeatherGeoCoding + f'?q={city}&limit=5&appid={resources.openWeatherAPIkey}')
    if geoResponse.status_code != 200:
        return resources.error_handling(geoResponse.status_code)
    if resources.json_is_empty(geoResponse.json()):
        return {"Error": "City Not Found"}
    
    # Extract lat and long
    cityLat = geoResponse.json()[0]["lat"]
    cityLon = geoResponse.json()[0]["lon"]

    # Get Weather data from Daily Aggregation API
    aggResponse = requests.get(resources.openWeatherAggregate + f'?lat={cityLat}&lon={cityLon}&date={date}&units=metric&appid={resources.openWeatherAPIkey}')
    if aggResponse.status_code != 200:
        return resources.error_handling(aggResponse.status_code)
    
    # Extract Humidity, Max Temperature, and Min Temperature 
    humidity = aggResponse.json()["humidity"]["afternoon"]
    maxTemp = aggResponse.json()["temperature"]["max"]
    minTemp = aggResponse.json()["temperature"]["min"]

    # Create Database Entry
    resources.db_add_row(con, city, date, maxTemp, minTemp, humidity)

    # Calculate Average Temp
    avgTemp = resources.calculate_avg_temp(maxTemp, minTemp)

    # Return Results
    return {"minTemp": minTemp, "maxTemp": maxTemp, "avgTemp": avgTemp, "humidity": humidity}