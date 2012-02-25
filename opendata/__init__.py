from flask import Flask
import settings

app = Flask('opendata')
app.config.from_object('opendata.settings')
app.debug = True

import views

