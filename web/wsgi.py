import sys
from os.path import dirname, abspath

# Add the directory this WSGI script is in to the Python PATH
#sys.path.append(abspath(dirname(__file__)))

# Import the "app" object from __init__.py in this package and use it as the WSGI application
from app import app as application

