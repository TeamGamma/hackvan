import sys

# Add the directory above this WSGI script to the Python PATH
sys.path.append('/home/dotcloud/code')

# Import the "app" object from __init__.py in this package and use it as the WSGI application
from web import app as application

