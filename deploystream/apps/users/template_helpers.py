from . import constants
from .models import OAuth
from deploystream import app


@app.template_filter('all_oauths')
def all_oauths(user):
    """Return all available oauths for the User.

    Returns all oauth information including those that the user hasn't
    connected to yet.
    """
    all_oauth = []
    for oauth_service in constants.OAUTHS:
        user_oauth = OAuth.query.filter_by(user_id=user.id,
                                           service=oauth_service).first()
        if user_oauth:
            all_oauth.append((oauth_service, user_oauth.service_username))
        else:
            all_oauth.append((oauth_service, None))

    return all_oauth


@app.template_filter('humanize_time')
def humanize_time(datetime):
    return datetime.strftime("%B %d, %Y")
