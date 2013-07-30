import tests


def setup():
    tests.recreate_db()
    tests.create_main_user()
