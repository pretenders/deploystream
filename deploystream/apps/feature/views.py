from functools import wraps

from flask import json, Response

from deploystream import app
from deploystream.apps.feature.lib import get_feature_info, get_all_features


def as_json(func):
    """
    Decorator that JSONifies result data.
    """
    @wraps(func)
    def _wrapped(*args, **kwargs):
        result = func(*args, **kwargs)
        native_result = [r.__dict__ for r in result]

        def nativify(data):
            """
            Convert stuff to native datatypes that can be JSON-encoded.

            This is a bespoke implementation that works with the types
            of objects we support.
            """
            if isinstance(data, basestring) or isinstance(data, int):
                return repr(data)
            elif isinstance(data, list) or isinstance(data, tuple):
                return [nativify(x) for x in data]
            elif isinstance(data, dict):
                return {
                    k: nativify(v)
                    for k, v in data.items() if not k.startswith('_')
                }
            elif data is None:
                return 'null'
            elif hasattr(data, '__dict__'):
                return nativify(data.__dict__)
            else:
                return '"{0}"'.format(data)

        return Response(json.dumps(nativify(native_result), indent=2),
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
