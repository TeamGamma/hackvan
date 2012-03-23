from web import app
from flaskext.sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://hackvan:hackvan@127.0.0.1:3306/hackvan'
db = SQLAlchemy(app)

