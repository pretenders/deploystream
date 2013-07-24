from deploystream import app
from deploystream.apps.feature.lib import get_feature_info, get_all_features
from deploystream.lib.transforms import as_json
from deploystream.decorators import needs_providers


@app.route('/features', methods=['GET'])
@needs_providers
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
