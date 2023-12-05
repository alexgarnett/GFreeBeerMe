import psycopg2.extras
import os
from src.database import init_db


def test_init_db():
    os.chdir(os.getcwd() + '/src/database')
    init_db.run()
    connection = psycopg2.connect("dbname='beer_app' user='postgres' password='password'")
    cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute('SELECT * FROM information ')
    beer_info = cursor.fetchone()
    assert beer_info['id'] == 1        # Beer ID = 1 for initializing with one beer


