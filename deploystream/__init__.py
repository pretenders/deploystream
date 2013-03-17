__version__ = '0.1'

from os import environ
from os.path import join, dirname
from flask import Flask

APP_DIR = dirname(__file__)
STATIC_DIR = join(APP_DIR, 'static')

app = Flask(__name__, static_folder=STATIC_DIR)

# Set configuration defaults from deploystream settings.
app.config.from_pyfile(join(APP_DIR, 'settings.py'))

# Override with anything in DEPLOYSTREAM_SETTINGS
if environ.get("DEPLOYSTREAM_SETTINGS"):
    app.config.from_envvar("DEPLOYSTREAM_SETTINGS")

try:
    from github_auth import APP_ID, APP_SECRET
    app.config.update({
        "GITHUB_APP_ID": APP_ID,
        "GITHUB_APP_SECRET": APP_SECRET,
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

from deploystream.apps.oauth import ensure_certifi_certs_installed
ensure_certifi_certs_installed()

# Initialise the plugins.
from providers import init_plugins
init_plugins(app.config['PROVIDERS'])

# set the secret key. Dummy secret for flask. When using in real life, have
# something that is actually a secret
app.secret_key = 'mysecret'

# Import any views we want to register here at the bottom of the file:
import deploystream.views  # NOQA
import deploystream.apps.feature.views  # NOQA
import deploystream.apps.oauth.github  # NOQA
