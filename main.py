from fastapi import FastAPI
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
    return {"city": city, "date": date}

    # Check that there is an entry in the database for this city and date.
    # If there is, query it and return those results

    # If there isn't, get the data and create a database entry

    # get data from GeoCoding API

    # Extract lat and long

    # Get Weather data from Daily Aggregation API

    # Extract Humidity, Max Temperature, and Min Temperature 

    # Create Database Entry

    # Calculate Average Temp

    # Return Results