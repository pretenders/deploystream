from sprintly_auth import TOKEN

GITHUB_CONFIG = {
    'organization': 'rockabox',
    'repositories': [
        ('rockabox', 'youtube-frames-v2'),
        ('rockabox', 'rbx_web'),
        ('rockabox', 'conf'),
    ],
}

SPRINTLY_CONFIG = {
    'user': 'carles.barrobes@rockaboxmedia.com',
    'token': TOKEN,
    'current': [
        {'status': 'in-progress', 'limit': 100},
        {'status': 'backlog', 'limit': 100},
    ],
    'products': [11356, 9134,]
}

GIT_CONFIG = {
}
