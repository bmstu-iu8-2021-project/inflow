#!/usr/bin/python3

import psycopg2




ENV = {
    "PG_USER": "inflow-client",
    "PG_PASS": "qwerty123",
    "PG_DB":"inflow",
    "PG_PORT":"5432",
}


if __name__ == "__main__":

    print(ENV)
    connection = psycopg2.connect(user=ENV["PG_USER"], password=ENV["PG_PASS"], port=ENV["PG_PORT"], database=ENV["PG_DB"])
    
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM tags")
