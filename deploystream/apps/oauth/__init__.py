oauth_suffix = "oauth-token"


def get_token(session, name):
    return session.get("{0}.{1}".format(name, oauth_suffix), '')


def set_token(session, name, value):
    session["{0}.{1}".format(name, oauth_suffix)] = value
