from web.database import db

class User(db.Model):
    username = db.Column(db.String(127), primary_key=True, nullable=False)
    password = db.Column(db.String(127), nullable=False)

