# GFreeBeerMe

This is a web app that will help users locate and access gluten free beer.

# About
This app built using separate containers for the database, the API, and the web application, so it is easy to install.

Users can see the list of beers in the database by navigating to the "Beers" tab, and can click on a beer to see more 
info about it. Users can also submit a beer under the "Contribute" tab.

# Installation
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
Ideas for future feature implementation include the ability to review beers, and add "encounters" where people can log 
a time and place where they have seen a certain beer, increasing the accessibility for other users.

Additionally, the app could be hosted online and potentially turned into a mobile app.

App in progress :arrows_counterclockwise:
