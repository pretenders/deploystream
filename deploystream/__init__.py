__version__ = '0.1'

from os import environ
from os.path import join, dirname
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

APP_DIR = dirname(__file__)
CONFIG_DIR = join(dirname(APP_DIR), 'config')
STATIC_DIR = join(APP_DIR, 'static')

app = Flask(__name__, static_folder=STATIC_DIR)

# Set configuration defaults from deploystream settings.
app.config.from_pyfile(join(CONFIG_DIR, 'settings.py'))

# Override with anything in DEPLOYSTREAM_SETTINGS
if environ.get("DEPLOYSTREAM_SETTINGS"):
    app.config.from_envvar("DEPLOYSTREAM_SETTINGS")

try:
    # TODO find a more appropriate way to initialise these (env vars?)
    from github_auth import APP_ID, APP_SECRET
    app.config.update({
        "oauth": {
            'github': (APP_ID, APP_SECRET)
        }
    })
except ImportError:
    print ("""
=============================================================================
* WARNING: Github authentication will not work.
* If you have access to the pretenders organisation, you should use the
  ``DeployStream (Pretenders-Test)`` application in Github.
* Take the Client ID and Client Secret from the web interface and assign them
  to APP_ID and APP_SECRET respectively inside github_auth.py somewhere on your
  Python path.
=============================================================================
""")
    # this is here so that tests can run on Travis, but we should have a nicer
    # way to set these up
    app.config.update({
        "oauth": {
            'github': ("", "")
        }
    })

from deploystream.lib import ensure_certifi_certs_installed
ensure_certifi_certs_installed()

# set the secret key. Dummy secret for flask. When using in real life, have
# something that is actually a secret
app.secret_key = 'mysecret'

db = SQLAlchemy(app)
# Initialise the providers.
from providers import init_providers
classes = init_providers(app.config['PROVIDERS'])

# Configure additional routes needed for oauth
from deploystream.apps.oauth.views import configure_oauth_routes
configure_oauth_routes(classes)

# Import any views we want to register here at the bottom of the file:
import deploystream.views  # NOQA
import deploystream.apps.feature.views  # NOQA

from deploystream.apps.users.views import mod as usersModule
app.register_blueprint(usersModule)
