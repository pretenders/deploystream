from flask import render_template, redirect, session, url_for

from deploystream import app


@app.route('/')
def homepage():
    return render_template('index.html')


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.clear()
    return redirect(url_for('homepage'))
