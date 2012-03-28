DEBUG = False
SECRET_KEY = 'dev_key_h8hfne89vm'
CSRF_ENABLED = True
CSRF_SESSION_LKEY = 'dev_key_h8asSNJ9s9=+'
APP_ID = '0'

TITLE = 'HackVan App'

TWILIO_ACCOUNT = "AC97ac1adb110109f39f1f68f8019155c2"
TWILIO_TOKEN = "0961b98002d01f307b7893ac695feadd"
TWILIO_NUMBER = "+17788002763"

try:
    import json
    envfile = '/home/dotcloud/environment.json'
    ENV = json.load(open(envfile, 'rU'))

    SQLALCHEMY_DATABASE_URI = ENV['DOTCLOUD_DB_MYSQL_URL'] + '/hackvan'
except:
    # Local settings
    SQLALCHEMY_DATABASE_URI = 'mysql://hackvan:hackvan@127.0.0.1:3306/hackvan'
