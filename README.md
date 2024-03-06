# GFreeBeerMe

This is a web app that will help users locate and access gluten free beer.

# Inspiration
As someone with Celiac Disease, one of the most common things I find myself missing is a good beer. I'm constantly 
traveling all over the US and Canada, and it is often difficult to find out which gluten free or gluten reduced beers 
are available in my area. For that reason, I decided to build an app to keep track of which beers are GF/GR, and where 
to find them. Now anyone can access the information contained and this app, and can help to build out the database with 
their own beers they have encountered.

# About
This app is deployed to a DigitalOcean server and is available online at GFreeBeer.Me.

This app built using separate containers for the database, the API, and the web application, so it is easy to install.
The application and API parts both make use of python's Flask library. The database is a PostgreSQL database. All of 
the features on this app use HTTP requests routed through the API to interact with the database. Additionally, location 
based searching is done with the help of Google's Geolocation API.

# Usage
Users can see the list of beers in the database by navigating to the "Beers" tab, and can click on a beer to see more 
info about it, including Encounters. An Encounter is a record of a user seeing the beer at a store, a bar, a brewery, 
etc. Encounters help users locate where they can purchase a beer. Users can submit a beer or encounter under the 
"Contribute" tab.

By using the "Locate" tab, users can perform a location based search to find Encounters near them. Using the "Search" 
tab, users can perform a text based search of all the beers in the database.

# Installation
If you desire, you can clone this repo and run the app locally.
Make sure you have the latest version of Docker properly installed. Then, clone into the repo
```
git clone https://github.com/alexgarnett/GFreeBeerMe
```

# Run the App
In the root directory, run
```
docker compose up
```
By default, the app is hosted at https://localhost:8000

# Testing
In order to perform testing, all containers must be running. Then, in the root directory, run pytest.
```
pytest
```

# Future Improvements
Future improvements for this app include filling out the database, and adding an embedded map to display location based 
search results.

App in progress :arrows_counterclockwise:
