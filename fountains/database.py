from fountains import app
from flaskext.sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://opendata:opendata@127.0.0.1:3306/opendata'
db = SQLAlchemy(app)

class Fountain(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # The location of the fountain
    latitude = db.Column(db.Float(), nullable=False)
    longitude = db.Column(db.Float(), nullable=False)

    # The open data feed this fountain was retrieved from (e.g. 'vancouver', 'flickr')
    source = db.Column(db.String(127), nullable=False)

    # Metadata about fountain from open data feed (city metadata, Flickr photo ID)
    extra_info = db.Column(db.String(255), default='')

    def __init__(self, latitude, longitude, source, extra_info):
        self.latitude = latitude
        self.longitude = longitude
        self.source = source
        self.extra_info = extra_info

    def __repr__(self):
        return '<Fountain at %d,%d from %s>' % \
                (self.latitude, self.longitude, self.source)


class FountainSearch(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # The location of the user
    user_latitude = db.Column(db.Float(), nullable=False)
    user_longitude = db.Column(db.Float(), nullable=False)

    # The location of the closest fountain found
    fountain_latitude = db.Column(db.Float(), nullable=False)
    fountain_longitude = db.Column(db.Float(), nullable=False)

    def __init__(self, user_position, fountain_position):
        self.user_latitude, self.user_longitude = user_position
        self.fountain_latitude, self.fountain_longitude = fountain_position

    def __repr__(self):
        return '<FountainSearch from %.3f,%.3f>' % \
                (self.user_latitude, self.user_longitude)



# Create all tables if they don't exist
db.create_all()

