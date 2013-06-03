from nose.tools import assert_equal

from sqlalchemy.exc import IntegrityError

from deploystream import db
from deploystream.apps.oauth.views import get_or_create_user_oauth
from deploystream.apps.users.models import User, OAuth


def test_logged_out_first_time_oauth_use():
    "Test when first signing in with external service"
    get_or_create_user_oauth(user_id=None,
        service_user_id='101',
        service_name='my-oauth-service',
        service_username='testuser')

    created = User.query.filter_by(username='testuser').first()
    assert_equal('testuser', created.username)
    assert_equal(1, len(created.oauth_keys))
    assert_equal('testuser', created.oauth_keys[0].service_username)
    assert_equal('my-oauth-service', created.oauth_keys[0].service)


def test_logged_out_first_time_oauth_name_clash():
    """
    Test when first signing in with external service with name clash.

    Tests the case where a user exists in deploystream with the same username
    as that found in the external service.
    """
    u = User(username='testclash')
    db.session.add(u)
    db.session.commit()
    try:
        get_or_create_user_oauth(user_id=None,
            service_user_id='102',
            service_name='my-oauth-service',
            service_username='testclash')

        created = User.query.filter_by(username='testclash').first()
    except IntegrityError:
        db.session.rollback()
        raise AssertionError("Not sure what we want to do in this case. "
            "Create a random username? Prompt for one?")


def test_logged_out_return_oauth_access():
    "Test that correct user is retrieved and logged in."
    first_created_id = get_or_create_user_oauth(user_id=None,
        service_user_id='103',
        service_name='my-oauth-service',
        service_username='test_return_user')
    # Now let's return logged out and see what happens.
    user_id = get_or_create_user_oauth(user_id=None,
        service_user_id='103',
        service_name='my-oauth-service',
        service_username='test_return_user')

    assert_equal(user_id, first_created_id)


def test_logged_in_and_attach_additional_oauth_information():
    "Test that an additional OAuth is added to the account"
    u = User(username='additional')
    db.session.add(u)
    db.session.commit()

    user_id = get_or_create_user_oauth(user_id=u.id,
        service_user_id='109',
        service_name='my-oauth-service',
        service_username='add-github')

    assert_equal(user_id, u.id)
    original_user = User.query.filter_by(username='additional').first()
    assert_equal('add-github', original_user.oauth_keys[0].service_username)
