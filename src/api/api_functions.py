"""
This script contains helper functions for the app,
and handles interacting with the database
"""
import flask
import psycopg2.extras
from werkzeug.exceptions import abort


def connect_to_database():
    # Connection returns query as RealDict
    try:
        connection = psycopg2.connect("dbname='beer_app' user='postgres' password='password'")
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        return connection, cursor
    except Exception as e:
        raise Exception("Error connecting to the database. " + str(e))


def get_beer_info(beer_id):
    try:
        connection, cursor = connect_to_database()
        cursor.execute('SELECT * FROM information '
                       'WHERE id = %s', (beer_id,)
                       )
        beer_info = cursor.fetchone()
        connection.close()
    except Exception as e:
        raise Exception("Error connecting to the database. " + str(e))

    if beer_info is None:
        abort(
            404,
            f"Beer with beer_id {beer_id} not found"
        )
    return beer_info


def get_all_beer_info():
    try:
        connection, cursor = connect_to_database()
        cursor.execute("SELECT * FROM information")
        all_beers = cursor.fetchall()
        all_beers = [dict(row) for row in all_beers]
        connection.close()
        return all_beers
    except Exception as e:
        raise Exception("Error connecting to the database. " + str(e))


def add_beer_to_db(beer: dict):
    try:
        connection, cursor, = connect_to_database()
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM information ORDER BY id DESC LIMIT 1")
        old_id = cursor.fetchone()[0]

        sql = "INSERT INTO information(name, manufacturer, " \
              "city, state, country, availability, gf_or_gr) " \
              "VALUES(%s, %s, %s, %s, %s, %s, %s);"
        cursor.execute(sql, (beer['name'], beer['manufacturer'],
                             beer['city'], beer['state'], beer['country'],
                             beer['availability'], beer['gf_or_gr'],))
        connection.commit()

        cursor.execute("SELECT id FROM information ORDER BY id DESC LIMIT 1")
        new_id = cursor.fetchone()[0]
        connection.close()
    except Exception as e:
        raise Exception("Error connecting to database." + str(e))

    response = flask.make_response()
    if new_id != old_id:
        response.status_code = 201
        response.reason = f"Successfully created {beer['name']}"
    else:
        response.status_code = 400
        response.reason = f"Error creating {beer['name']}"

    return response
