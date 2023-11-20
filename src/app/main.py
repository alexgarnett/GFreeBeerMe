"""
This is the Gluten Free Beer app
This script uses beer_api.py to access the beer database
By default, this script looks for the API at http://127.0.0.1:8080
This IP/port combo can be changed when running this script at the command line
To specify a different IP/port combo, run:
```
python3 main.py [API_IP] [API_PORT]
```
Example
```
python3 main.py 192.0.0.1 5000
```
"""

import sys
from flask import Flask, render_template, request
import requests
from flask_mail import Mail, Message


if len(sys.argv) > 2:
    try:
        API_IP = f'http://{sys.argv[1]}:'
        API_PORT = str(sys.argv[2])
    except Exception as e:
        print('Invalid command line arguments')
        print(e)
else:
    API_IP = 'http://127.0.0.1:'
    API_PORT = '8080'

print(f'Looking for API at {API_IP}{API_PORT}')


app = Flask(__name__)
mail = Mail(app)


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/about')
def about_page():
    return render_template('about.html')


@app.route('/beers', methods=['GET'])
def all_beers_page():
    request_url = f'{API_IP}{API_PORT}/api/beers'
    response = requests.get(request_url)
    all_beers = response.json()
    return render_template('all_beers.html', all_beers=all_beers)


@app.route('/contribute')
def contribute_page():
    return render_template('contribute.html')


@app.route('/contribute/submit', methods=['POST'])
def submit_contribution():
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

        print(name + " " + manufacturer + " " + city + " " + state + " " + country + " " + availability + " " +
              gf_or_gr + " " + comments + " " + email)
        # todo: enter data into DB
        msg_to_creator = Message("Submission from BeerApp received", sender=email,
                                 recipients="alexgarnett_1@hotmail.com")
        msg_to_creator.body = 'Submission received from {}\nBeer name: {}\nManufacturer: {}\nCity: {}\n' \
                              'State: {}\nCountry: {}\nAvailability: {}\nGluten content: {}\nComments: {}\n'\
            .format(email, name, manufacturer, city, state, country, availability, gf_or_gr, comments)

        msg_to_contributor = Message("Thank you for your contribution to the BeerApp!!", sender='admin@beerapp.com',
                                recipients=email)
        msg_to_contributor.body = "No really, thank you!!"

        mail.send(msg_to_creator)
        mail.send(msg_to_contributor)

        return render_template("contribution_processed.html")


@app.route('/beers/<int:beer_id>', methods=['GET'])
def beer_info_page(beer_id: int):
    request_url = f'{API_IP}{API_PORT}/api/beers/{beer_id}'
    response = requests.get(request_url)
    beer_info = response.json()
    return render_template('beer_info.html', beer_info=beer_info)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)

