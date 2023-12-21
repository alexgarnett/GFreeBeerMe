"""
This script contains helper functions for the app,
and handles interacting with the database
"""
import os
import flask
import psycopg2.extras
from werkzeug.exceptions import abort

DB_NAME = os.getenv('POSTGRES_DB', default='beer_app')
USER = os.getenv('POSTGRES_USER', default='postgres')
PASSWORD = os.getenv('POSTGRES_PASSWORD', default='password')
DB_HOST = os.getenv('DB_HOST', default='localhost')
DB_PORT = os.getenv('DB_PORT', default='5432')


def connect_to_database():
    # Connection returns query as RealDict
    try:
        connection = psycopg2.connect(f"dbname={DB_NAME} user={USER} "
                                      f"password={PASSWORD} host={DB_HOST} "
                                      f"port={DB_PORT}")
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        return connection, cursor
    except Exception as e:
        raise Exception("Error connecting to the database. " + str(e))


def get_beer_info(beer_id):
    try:
        connection, cursor = connect_to_database()
        cursor.execute('SELECT * FROM information '
                       'WHERE id = %s;', (beer_id,)
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
        cursor.execute("SELECT * FROM information ORDER BY manufacturer ASC;")
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


def get_encounters(beer_id: int):
    try:
        connection, cursor = connect_to_database()
        cursor.execute('SELECT * FROM encounters '
                       'WHERE id = %s'
                       'ORDER BY date_of DESC;', (beer_id,)
                       )
        encounters = cursor.fetchall()
        connection.close()
    except Exception as e:
        print("Exception when attempting to fetch encounters: " + str(e))
        encounters = None

    return encounters


def get_all_encounters():
    try:
        connection, cursor = connect_to_database()
        cursor.execute('SELECT encounters.id, information.name, '
                       'information.manufacturer, information.gf_or_gr, '
                       'encounters.date_of, encounters.location, '
                       'encounters.content '
                       'FROM encounters '
                       'INNER JOIN information ON encounters.id=information.id '
                       'ORDER BY date_of DESC;')
        encounters = cursor.fetchall()
        # encounters = [dict(row) for row in encounters]
        connection.close()

    except Exception as e:
        print("Exception when attempting to fetch encounters: " + str(e))
        encounters = None

    return encounters
