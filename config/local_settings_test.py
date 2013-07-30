from os import path

GITHUB_CONFIG = {
    'repositories': [
        ('pretenders', 'deploystream'),
        ('pretenders', 'pretenders'),
        ('txels', 'autojenkins'),
        ('txels', 'ddt'),
        ('txels', 'apitopy'),
    ],
}

SPRINTLY_CONFIG = {
    'user': 'carles.barrobes@rockaboxmedia.com',
    'token': 'iwonttell',
    'current': [
        {'status': 'in-progress', 'limit': 100},
        {'status': 'backlog', 'limit': 100},
    ],
}

GIT_CONFIG = {
}

CSRF_ENABLED = False
TEST_DB_LOCATION = path.join(path.abspath(path.dirname(__file__)), 'test.db')
SQLALCHEMY_DATABASE_URI = ('sqlite:///' + TEST_DB_LOCATION)
