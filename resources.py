import statistics

#### COMMON VARIABLES ####

# API Keys
openWeatherAPIkey = "155b1cc2b1ccefcb5a370d6d01687f12"

# API Endpoints
openWeatherGeoCoding = 'http://api.openweathermap.org/geo/1.0/direct'
openWeatherAggregate = 'https://api.openweathermap.org/data/3.0/onecall/day_summary'



#### COMMON FUNCTIONS ####

def db_confirm_database_exists(cur):
    # Return True if the database exists
    query = 'SELECT name FROM sqlite_master'
    queryResponse = cur.execute(query)
    if queryResponse.fetchone() == 'weather':
        return True

def db_check_record_exists(con, city, date):
    # Return True if a record exists
    query = (f"SELECT * FROM weather WHERE city_name='{city}' AND date='{date}'")
    queryResult = con.execute(query).fetchone()
    if queryResult is not None:
        return True

def db_add_row(con, city, date, max, min, hum):
    # Add a record to the table
    query = (f"INSERT INTO weather (city_name, date, max_temp, min_temp, humidity) VALUES ('{city}', '{date}', '{max}', '{min}', '{hum}')")
    con.execute(query)
    con.commit()

def db_return_row(con, city, date):
    # Return the values for a specified city and date record
    query = (f"SELECT * FROM weather WHERE city_name='{city}' AND date='{date}'")
    queryResult = con.execute(query).fetchone()
    if queryResult is not None:
        return queryResult