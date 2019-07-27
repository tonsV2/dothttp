import email
from io import StringIO
from urllib.parse import urlparse
import http.client
import ssl
from pprint import pprint

"""
Request URI needs to be absolute
Host header will be overwritten
HTTP Version is ignored
"""

file = "postman.http"
file = "request.http"
file = "request2.http"
file = "postman-post.http"
with open(file, 'r') as f:
    request_string = f.read()



request_line, headers_and_body = request_string.split('\n', 1)
message = email.message_from_file(StringIO(headers_and_body))

method, request_uri, http_version = request_line.split(' ')
headers = dict(message.items())
message_body = message.get_payload()



parsed = urlparse(request_uri)
TARGET_IP = parsed.netloc
path = parsed.path
if parsed.query:
    path = '%s?%s' % (path, parsed.query)
connection = {}
if parsed.scheme == 'http':
    connection = http.client.HTTPConnection(TARGET_IP)
elif parsed.scheme == 'https':
    connection = http.client.HTTPSConnection(TARGET_IP, timeout=8, context=ssl._create_unverified_context())
connection.request(method, path, message_body, headers={'Host': parsed.netloc})
response = connection.getresponse()
body = response.read().decode('utf8')
response.close()
connection.close()

print("%s %s %s" % (http_version, response.status, http.client.responses[response.status]))
response_headers = response.headers
for key in response_headers:
    print("%s: %s" % (key, response_headers[key]))
pprint(body)
