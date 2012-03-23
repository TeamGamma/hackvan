from fountains import app
from fountains.database import db, Fountain, FountainSearch
from flask import render_template
import json
from fountains.recommendation import find_closest_fountain
from fountains.recommendation import recommend_next_location

import settings

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html', settings=settings)

@app.route('/map', methods=['GET'])
def map():
    return render_template('map.html', settings=settings)

@app.route('/fountains', methods=['GET'])
def fountains():
    fountains = Fountain.query.all()
    return json.dumps([
        {"latitude":fountain.latitude, "longitude":fountain.longitude}
        for fountain in fountains])


@app.route('/fountains/closest/<latitude>,<longitude>', methods=['GET'])
def closest_fountain(latitude, longitude):
    latitude = float(latitude)
    longitude = float(longitude)
    fountains = Fountain.query.all()
    coords = [(fountain.latitude, fountain.longitude)
              for fountain in fountains]
    point = find_closest_fountain((latitude, longitude), coords)

    # Store a FountainSearch for this search
    fs = FountainSearch(
            user_position=(latitude, longitude), 
            fountain_position=point)
    db.session.add(fs)
    db.session.commit()

    return json.dumps({"latitude": point[0], "longitude": point[1]})


@app.route('/fountains/recommendations', methods=['GET'])
def recommended_fountains():
    searches = FountainSearch.query.all()

    coords = [(search.user_latitude, search.user_longitude,
               search.fountain_latitude, search.fountain_longitude)
               for search in searches]

    point = recommend_next_location(coords)

    return json.dumps({"latitude": point[0], "longitude": point[1]})



