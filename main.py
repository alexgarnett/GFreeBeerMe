"""This is the Gluten Free Beer app"""

import psycopg2.extras
from flask import Flask, render_template

app = Flask(__name__)
@app.route('/')

def main():
    conn = psycopg2.connect("dbname='beer_app' user='postgres' password='password'")
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM information")  # QUERY
    all_beers = cur.fetchall()
    conn.close()

    return render_template('index.html', all_beers=all_beers)

if __name__ == '__main__':
    main()

