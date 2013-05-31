def load_user_to_session(session, user):
    session['user_id'] = user.id
    session['user_name'] = user.name
