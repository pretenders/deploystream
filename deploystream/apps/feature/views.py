from flask import render_template

from deploystream import app


@app.route('/feature/<feature_id>', methods=['GET'])
def view_feature(feature_id):

    return render_template('feature.html', feature_id=feature_id)
