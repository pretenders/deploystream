from flask import session

from deploystream import app
from deploystream.providers import get_providers


def needs_providers(func):
    "Decorator to make sure we have providers available for this request"
    def new_func(*args, **kwargs):
        # For now, get the user specific conf from settings. This will
        # need to change when we're DB-driven.
        config = (
                app.config['USER_SPECIFIC_INFO']['provider_config'])

        providers = get_providers(config, session)
        return func(providers=providers, *args, **kwargs)
    return new_func
