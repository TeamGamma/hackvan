from opendata import app
from flaskext.sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://opendata:opendata@127.0.0.1:3306/opendata'
db = SQLAlchemy(app)

class Fountain(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float())
    longitude = db.Column(db.Float())

    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return '<Fountain at %d,%d>' % (self.latitude, self.longitude)


# Create all tables if they don't exist
db.create_all()

