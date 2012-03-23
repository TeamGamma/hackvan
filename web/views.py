from web import app
from flask import render_template

import settings

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html', settings=settings)
