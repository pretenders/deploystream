VERSION = '0.1'
from os import environ
from os.path import join, dirname
from flask import Flask

app = Flask(__name__)

# Set configuration defaults from deploystream settings.
app.config.from_pyfile(join(dirname(__file__), 'settings.py'))

# Override with anything in DEPLOYSTREAM_SETTINGS
if environ.get("DEPLOYSTREAM_SETTINGS"):
    app.config.from_envvar("DEPLOYSTREAM_SETTINGS")

# Import any views we want to register here at the bottom of the file:
import deploystream.apps.feature.views
