#!/usr/bin/env python
from web import app

if __name__ == '__main__':
    # Refresh database on restarting server when in debug mode
    print 'Clearing database and installing fixtures'
    from web.fixtures import load_fixtures
    load_fixtures()

    app.run(debug=True)
