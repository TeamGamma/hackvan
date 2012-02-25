from opendata import app
from flask import (
    request, url_for,
    make_response, redirect, abort, session, flash,
    render_template,
)
import settings

@app.route('/', methods=['GET', 'POST'])
def command_index():
    return 'hello world'


