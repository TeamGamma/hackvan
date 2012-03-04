from fountains import app
from fountains.database import db, Fountain
from flask import (
    request, url_for,
    make_response, redirect, abort, session, flash,
    render_template,
)
import json
from fountains.recommendation import find_closest_fountain

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
    return json.dumps({"latitude":point[0], "longitude":point[1]})



