import jsonpickle

from deploystream import app
from deploystream.apps.feature.lib import get_feature_info


@app.route('/feature/<feature_id>', methods=['GET'])
def view_feature(feature_id):
    feature = get_feature_info(feature_id)
    return jsonpickle.encode(feature)
