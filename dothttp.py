import email
from io import StringIO
from urllib.parse import urlparse
from http.client import HTTPConnection, HTTPSConnection
import ssl
from pprint import pprint
import click


@click.command()
@click.argument('files', nargs=-1, type=click.File('r'), required=True)
def cli(files):
    for file in files:
        # Parse http request
        request_line, headers_and_body = file.read().split('\n', 1)
        message = email.message_from_file(StringIO(headers_and_body))

        request_line_split = request_line.split(' ')
        if len(request_line_split) == 3:
            method, request_uri, http_version = request_line_split
        elif len(request_line_split) == 2:
            method, request_uri = request_line_split
            http_version = "HTTP/1.1"
        headers = dict(message.items())
        message_body = message.get_payload()

        # Perform http request
        parsed = urlparse(request_uri)
        hostname = parsed.netloc
        path = parsed.path
        if parsed.query:
            path = '%s?%s' % (path, parsed.query)
        connection = {}
        if parsed.scheme == 'http':
            connection = HTTPConnection(hostname)
        elif parsed.scheme == 'https':
            connection = HTTPSConnection(hostname, timeout=8, context=ssl._create_unverified_context())
        headers['Host'] = parsed.netloc
        connection.request(method, path, message_body, headers=headers)
        response = connection.getresponse()
        body = response.read().decode('utf8')
        response.close()
        connection.close()

        # Print http response
        print("%s %s %s" % (http_version, response.status, http.client.responses[response.status]))
        response_headers = response.headers
        for key in response_headers:
            print("%s: %s" % (key, response_headers[key]))
        pprint(body)
