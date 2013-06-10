def load_user_to_session(session, user):
    session['user_id'] = user.id
    session['user_name'] = user.username


def get_user_id_from_session(session):
    try:
        return session['user_id']
    except KeyError:
        return None
