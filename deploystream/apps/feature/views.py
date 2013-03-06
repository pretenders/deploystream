from functools import wraps

from flask import json, Response

from deploystream import app
from deploystream.apps.feature.lib import get_feature_info, get_all_features
from deploystream.lib.transforms import nativify


def as_json(func):
    """
    Decorator that JSONifies result data.
    """
    @wraps(func)
    def _wrapped(*args, **kwargs):
        result = func(*args, **kwargs)
        return Response(json.dumps(nativify(result), indent=2),
                        mimetype='application/json')

    return _wrapped


@app.route('/features', methods=['GET'])
@as_json
def list_features():
    features = get_all_features()
    return features


@app.route('/feature/<feature_id>', methods=['GET'])
@as_json
def view_feature(feature_id):
    feature = get_feature_info(feature_id)
    return feature
