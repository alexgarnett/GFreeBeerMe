"""
This is the Gluten Free Beer app
This script uses beer_api.py to access the beer database
By default, this script looks for the API at http://localhost:8080
"""

import os
import sys
from flask import Flask, render_template, request, abort
import requests
from geopy.geocoders import Nominatim
# from flask_mail import Mail

API_HOST = f"http://{os.getenv('API_HOST', default='localhost')}"
API_PORT = os.getenv('API_PORT', default='8080')

print(f'Looking for API at {API_HOST}:{API_PORT}')


app = Flask(__name__)
# mail = Mail(app)


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/about')
def about_page():
    return render_template('about.html')


@app.route('/beers', methods=['GET'])
def all_beers_page():
    request_url = f'{API_HOST}:{API_PORT}/api/beers'
    response = requests.get(request_url)
    all_beers = response.json()
    return render_template('all_beers.html', all_beers=all_beers)


@app.route('/beers/<int:beer_id>', methods=['GET'])
def beer_info_page(beer_id: int):
    beer_id_url = f'{API_HOST}:{API_PORT}/api/beers/{beer_id}'
    response = requests.get(beer_id_url)
    beer_info = response.json()
    gluten_content = beer_info['gf_or_gr']
    if gluten_content == 'GF':
        beer_info['gf_or_gr'] = 'Gluten Free'
    elif gluten_content == 'GR':
        beer_info['gf_or_gr'] = 'Gluten Reduced'

    encounters_url = beer_id_url + '/encounters'
    encounters_response = requests.get(encounters_url)
    encounters = encounters_response.json()
    # Format data for the encounters
    for encounter in encounters:
        date = encounter['date_of']
        date = date.split(' ')
        encounter['date_of'] = date[0] + ' ' + date[1] + ' ' + date[2] + ' ' + date[3]
        coordinates = encounter['location']
        coordinates = coordinates.split(',')
        lat = coordinates[0][1:]
        lon = coordinates[1][:-1]
        geolocator = Nominatim(user_agent="beer_app")
        geolocation = geolocator.reverse((float(lat), float(lon)))
        if geolocation is not None:
            encounter['location'] = geolocation.address
        else:
            encounter['location'] = lat + 'N, ' + lon + 'W'

    return render_template('beer_info.html', beer_info=beer_info, encounters=encounters)


@app.route('/contribute')
def contribute_page():
    return render_template('contribute.html')


@app.route('/contribute/submit', methods=['POST'])
def submit_contribution():
    request_url = f'{API_HOST}:{API_PORT}/api/contribute'
    if request.method == 'POST':
        name = request.form.get('name')
        manufacturer = request.form.get('manufacturer')
        city = request.form.get('city')
        state = request.form.get('state')
        country = request.form.get('country')
        availability = request.form.get('availability')
        gf_or_gr = request.form.get('gf_or_gr')
        comments = request.form.get('comments')
        email = request.form.get('email')

        beer_dict = {
            'name': name,
            'manufacturer': manufacturer,
            'city': city,
            'state': state,
            'country': country,
            'availability': availability,
            'gf_or_gr': gf_or_gr
        }
        response = requests.post(request_url, json=beer_dict)

        # msg_to_creator = Message("Submission from BeerApp received", sender=email,
        #                          recipients="alexgarnett_1@hotmail.com")
        # msg_to_creator.body = 'Submission received from {}\nBeer name: {}\nManufacturer: {}\nCity: {}\n' \
        #                       'State: {}\nCountry: {}\nAvailability: {}\nGluten content: {}\nComments: {}\n'\
        #     .format(email, name, manufacturer, city, state, country, availability, gf_or_gr, comments)
        #
        # msg_to_contributor = Message("Thank you for your contribution to the BeerApp!!", sender='admin@beerapp.com',
        #                         recipients=email)
        # msg_to_contributor.body = "No really, thank you!!"
        #
        # mail.send(msg_to_creator)
        # mail.send(msg_to_contributor)

        if response.status_code == 201:
            return render_template("contribution_processed.html")
        else:
            abort(401)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)

