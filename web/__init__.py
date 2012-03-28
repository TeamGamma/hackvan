from flask import Flask
import settings

app = Flask('web')
app.config.from_object('web.settings')

import views

