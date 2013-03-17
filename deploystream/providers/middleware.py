from flask import session

from deploystream.providers import get_providers


class ProviderLoadingMiddleware(object):
    """
    Middleware that loads relevant providers into the current session.
    """

    def __init__(self, app, *args, **kwargs):
        self.app = app

    def __call__(self, environ, start_response):
        if not session.get('providers'):
            # For now, get the user specific conf from settings. This will
            # need to change when we're DB-driven.
            providers = (
                self.app.config['USER_SPECIFIC_INFO']['provider_config'])

            session['providers'] = get_providers(providers, session)
        return self.app(environ, start_response)
