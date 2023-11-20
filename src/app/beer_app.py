"""Helper functions for the app"""

import psycopg2.extras
from werkzeug.exceptions import abort


def connect_to_database():
    # Connection returns query as RealDict
    connection = psycopg2.connect("dbname='beer_app' user='postgres' password='password'")
    cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    return connection, cursor


def get_beer_info(beer_id):
    connection, cursor = connect_to_database()
    cursor.execute('SELECT * FROM information WHERE id = %s', (beer_id,))
    beer_info = cursor.fetchone()
    connection.close()
    if beer_info is None:
        abort(404)
    return beer_info


def get_all_beer_info():
    connection, cursor = connect_to_database()
    cursor.execute("SELECT * FROM information")  # QUERY
    all_beers = cursor.fetchall()
    all_beers = [dict(row) for row in all_beers]
    connection.close()
    return all_beers
