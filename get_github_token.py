#!/usr/bin/env python
from github3 import authorize
from getpass import getpass

user = raw_input("Username: ")
password = ''

while not password:
    password = getpass('Password for {0}: '.format(user))

note = 'Deploystream'
note_url = 'http://deploystream.com'
scopes = ['user', 'repo']

auth = authorize(user, password, scopes, note, note_url)

filename = 'github_auth.py'
print("Writing token to {0}...".format(filename))

with open(filename, 'w') as fd:
    fd.write("TOKEN = '{0}'\n".format(auth.token))
    fd.write("ID = {0}\n".format(auth.id))
