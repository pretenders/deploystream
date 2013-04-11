from functools import wraps

from flask import session

from deploystream import app
from deploystream.exceptions import MissingTokenException
from deploystream.providers import get_providers
from deploystream.apps import oauth


def needs_providers(func):
    "Decorator to make sure we have providers available for this request"
    @wraps(func)
    def _wrapped(*args, **kwargs):
        # For now, get the user specific conf from settings. This will
        # need to change when we're DB-driven.
        config = (
            app.config['USER_SPECIFIC_INFO']['provider_config']
        )
        try:
            providers = get_providers(config, session)
            return func(providers=providers, *args, **kwargs)
        except MissingTokenException, te:
            # If we haven't got a required token, let's stop here and
            # go and get it.
            return oauth.views.start_token_processing(te.missing_token)
    return _wrapped
