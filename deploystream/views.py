from flask import render_template

from deploystream import app


@app.route('/')
def homepage():
    return render_template('index.html')
