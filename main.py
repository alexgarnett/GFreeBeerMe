"""This is the Gluten Free Beer app"""

import psycopg2.extras
from flask import Flask, render_template, views
from werkzeug.exceptions import abort


class BeerApp:

    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect_to_database(self):
        # Connection returns query as RealDict
        self.connection = psycopg2.connect("dbname='beer_app' user='postgres' password='password'")
        self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    def get_beer_info(self, beer_id):
        self.connect_to_database()
        self.cursor.execute('SELECT * FROM information WHERE id = %s', (beer_id,))
        beer_info = self.cursor.fetchone()
        self.connection.close()
        if beer_info is None:
            abort(404)
        return beer_info

    def get_all_beer_info(self):
        self.connect_to_database()
        self.cursor.execute("SELECT * FROM information")  # QUERY
        all_beers = self.cursor.fetchall()
        self.connection.close()
        return all_beers


beer_app = BeerApp()
app = Flask(__name__)


@app.route('/')
def main():
    # beer_app = BeerApp()
    all_beers = beer_app.get_all_beer_info()

    return render_template('index.html', all_beers=all_beers)


@app.route('/<int:beer_id>')
def beer_info_page(beer_id):
    beer_info = beer_app.get_beer_info(beer_id)
    return render_template('beer_info.html', beer_info=beer_info)


if __name__ == '__main__':
    main()

