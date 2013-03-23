from sprintly_auth import TOKEN

GITHUB_CONFIG = {
    'repositories': [
        ('rockabox', 'rbx_web'),
        ('rockabox', 'conf'),
        ('rockabox', 'youtube-frames'),
    ],
}

SPRINTLY_CONFIG = {
    'user': 'carles.barrobes@rockaboxmedia.com',
    'token': TOKEN,
    'current': [
        {'status': 'in-progress', 'limit': 100},
        {'status': 'backlog', 'limit': 100},
    ],
}

GIT_CONFIG = {
}
