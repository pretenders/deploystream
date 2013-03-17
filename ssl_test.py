
url = 'https://github.com/'

import httplib2
h = httplib2.Http(".cache")#, disable_ssl_certificate_validation=True)
resp, content = h.request(url, "GET")
print resp, content
