from functools import wraps

from flask import json, Response

from deploystream import app
from deploystream.apps.feature.lib import get_feature_info, get_all_features
from deploystream.lib import cache
from deploystream.lib.transforms import nativify
from deploystream.decorators import needs_providers


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
@needs_providers
@cache.cached()
@as_json
def list_features(providers):
    features = get_all_features(providers)
    return features


@app.route('/features/<feature_id>', methods=['GET'])
@needs_providers
@as_json
def view_feature(feature_id, providers):
    feature = get_feature_info(feature_id, providers)
    return feature
