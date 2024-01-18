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
from geopy import distance
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
        format_encounter_data(encounter)

    return render_template('beer_info.html', beer_info=beer_info, encounters=encounters)


@app.route('/contribute')
def contribute_page():
    return render_template('contribute_page.html')


@app.route('/contribute/beer')
def contribute_beer_page():
    return render_template('beer_form.html')


@app.route('/contribute/encounter')
def contribute_encounter_page():
    return render_template('encounter_form.html')


@app.route('/contribute/beer/submit', methods=['POST'])
def submit_contribution():
    request_url = f'{API_HOST}:{API_PORT}/api/contribute'
    if request.method == 'POST':
        name = request.form.get('name')
        manufacturer = request.form.get('manufacturer')
        city = request.form.get('city', '')     # Adding default '' to avoid Nonetype errors
        state = request.form.get('state', '')
        country = request.form.get('country', '')
        availability = request.form.get('availability', 'Unknown')
        gf_or_gr = request.form.get('gf_or_gr', 'Unknown')
        comments = request.form.get('comments', '')
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

        # None types will cause errors
        for key, val in beer_dict.items():
            if val is None:
                beer_dict[key] = ""

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


@app.route('/contribute/encounter/submit', methods=['POST'])
def submit_encounter():
    post_url = f'{API_HOST}:{API_PORT}/api/contribute_encounter'
    if request.method == 'POST':
        name = request.form.get('name')
        manufacturer = request.form.get('manufacturer')
        date_of = request.form.get('date_of')
        user_location = request.form.get('user_location', '')
        address = request.form.get('address', '')
        content = request.form.get('content', '')

        # If we did not get user coordinates, attempt to find them from Geolocator
        if user_location is '':
            geolocator = Nominatim(user_agent="beer_app")
            geolocation = geolocator.geocode(address)
            if geolocation is None:
                return "Unable to find a location with that address, please try again"
            else:
                user_location = str((geolocation.latitude, geolocation.longitude))

        # Search database for beer with same name and manufacturer
        search_url = f'{API_HOST}:{API_PORT}/api/search?name={name}&manufacturer={manufacturer}'
        result = requests.get(search_url).json()
        if len(result) == 0:
            return "Unable to find a beer in our database with that name and manufacturer. Please " \
                   "first submit a new beer entry, then resubmit your encounter"

        matching_beer = result[0]
        beer_id = matching_beer['id']

        encounter_dict = {
            'id': beer_id,
            'date_of': date_of,
            'location': user_location,
            'address': address,
            'content': content
        }
        print(encounter_dict)
        response = requests.post(post_url, json=encounter_dict)

        if response.status_code == 201:
            return render_template("contribution_processed.html")
        else:
            abort(401)


@app.route('/locate')
def locate_page():
    return render_template("locate_page.html")


@app.route('/locate/results', methods=['POST'])
def locate_results():
    if request.method == 'POST':
        geolocator = Nominatim(user_agent="beer_app")

        user_location = request.form.get('user_location')
        city = request.form.get('city')
        state = request.form.get('state')
        search_radius = int(request.form.get('distance'))

        if user_location:
            center_coordinates = str_coordinates_to_float_tuple(user_location)
            search_location = user_location

        else:
            geolocation = geolocator.geocode(city + ', ' + state)
            center_coordinates = (geolocation.latitude, geolocation.longitude)
            search_location = city + ', ' + state

        # Call all encounters endpoint of api
        all_encounters_url = f'{API_HOST}:{API_PORT}/api/all_encounters'
        all_encounters = requests.get(all_encounters_url).json()

        # Structure for filtered_encounters
        # [{'name': 'Redbridge',
        #   'manufacturer': 'Anheuser-Busch',
        #   'encounters': [encounter1, encounter2, ...]},
        #  {'name': 'Copperpoint Lager',
        #   'manufacturer': 'Copperpoint',
        #   'encounters': [encounter1, encounter2, ...]}]

        # Filter by distance
        filtered_encounters = []
        for encounter in all_encounters:
            encounter_coordinates = str_coordinates_to_float_tuple(encounter['location'])
            distance_to_encounter = distance.distance(center_coordinates, encounter_coordinates).miles
            if distance_to_encounter <= search_radius:
                format_encounter_data(encounter)
                encounter['distance'] = round(distance_to_encounter, 1)
                if len(filtered_encounters) < 1:
                    new_entry = {'name': encounter['name'],
                                 'manufacturer': encounter['manufacturer'],
                                 'id': encounter['id'],
                                 'encounters': [encounter]}
                    filtered_encounters.append(new_entry)
                else:
                    for filtered in filtered_encounters:
                        if filtered['id'] == encounter['id']:
                            filtered['encounters'].append(encounter)
                        else:
                            new_entry = {'name': encounter['name'],
                                         'manufacturer': encounter['manufacturer'],
                                         'id': encounter['id'],
                                         'encounters': [encounter]}
                            filtered_encounters.append(new_entry)

        # return filtered_encounters
        # Render template with the filtered list of encounters
        return render_template("encounters.html", encounters=filtered_encounters,
                               search_location=search_location,
                               search_radius=search_radius)


def str_coordinates_to_float_tuple(coordinates: str) -> tuple:
    stripped_parenthesis = coordinates.strip('()')
    split = stripped_parenthesis.split(',')
    float_tuple = (float(split[0]), float(split[1]))
    return float_tuple


def format_encounter_data(encounter):
    date = encounter['date_of']
    date = date.split(' ')
    encounter['date_of'] = date[0] + ' ' + date[1] + ' ' + date[2] + ' ' + date[3]
    coordinates = encounter['location']
    coordinates = coordinates.split(',')
    lat = coordinates[0][1:]
    lon = coordinates[1][:-1]
    encounter['location'] = lat + 'N, ' + lon + 'W'
    geolocator = Nominatim(user_agent="beer_app")
    geolocation = geolocator.reverse((float(lat), float(lon)))
    if geolocation is not None:
        encounter['address'] = geolocation.address
    else:
        encounter['address'] = 'Not available'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)

