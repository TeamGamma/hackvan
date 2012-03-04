from flask import Flask
import settings

app = Flask('fountains')
app.config.from_object('fountains.settings')
app.debug = True

import views

