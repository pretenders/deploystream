VERSION = '0.1'
from flask import Flask

app = Flask(__name__)

# Import any views we want to register here at the bottom of the file:
import deploystream.apps.feature.views
