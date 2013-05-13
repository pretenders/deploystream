import os.path

TEST_DATA = os.path.join(os.path.dirname(__file__), 'data')


def load_fixture(filename):
    with file(os.path.join(TEST_DATA, filename)) as f:
        contents = f.read()
    return contents


DEFAULT_HIERARCHY_REGEXES = [
        'master',
        'develop',
        'story/{FEATURE_ID}(/[a-z]*)?',
        'dev/{FEATURE_ID}/[a-z]*',
        '[a-zA-Z]*/{FEATURE_ID}/[a-zA-Z]*'
]
