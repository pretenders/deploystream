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

# Initialise the plugins.
from providers import init_plugins
init_plugins()

# Import any views we want to register here at the bottom of the file:
import deploystream.views  # NOQA
import deploystream.apps.feature.views  # NOQA
