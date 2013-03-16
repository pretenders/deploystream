
url = 'https://github.com/login/oauth/access_token?client_secret=326b61bb74681f40ebbe55946a558988fe9e6108&code=eba85f217984c2694d00&client_id=093793e99aa26166c560&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2Foauth-authorized%2F'

import httplib2
h = httplib2.Http(".cache")#, disable_ssl_certificate_validation=True)
resp, content = h.request(url, "GET")
print resp, content
