from functools import wraps

from flask import request
from werkzeug.contrib.cache import SimpleCache


cache = SimpleCache()
EXPIRY_SECONDS = 5 * 60


def cached(timeout=EXPIRY_SECONDS, key='view/%s'):
    """
    A decorator for caching views.

    Source: http://flask.pocoo.org/docs/patterns/viewdecorators/

    With a little additional work it could be made into a generic caching
    decorator for other functions that return pickleable data.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            cache_key = key % request.path
            rv = cache.get(cache_key)
            if rv is not None:
                return rv
            rv = f(*args, **kwargs)
            cache.set(cache_key, rv, timeout=timeout)
            return rv
        return decorated_function
    return decorator


def activate_requests_caching():
    """
    Call once to activate caching for all HTTP GET issued by 'requests'
    """
    import requests_cache
    requests_cache.install_cache(expire_after=EXPIRY_SECONDS)
