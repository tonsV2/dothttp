import email
import json
import ssl
from http.client import HTTPConnection, HTTPSConnection
from io import StringIO
from urllib.parse import urlparse

import click
from pygments import highlight, lexers, formatters
from termcolor import colored


@click.command()
@click.argument('files', nargs=-1, type=click.File('r'), required=True)
def cli(files):
    for file in files:
        request(file)


def request(file):
    # Parse http request
    request_line, headers_and_body = file.read().split('\n', 1)
    message = email.message_from_file(StringIO(headers_and_body))

    method, request_uri = request_line.split(' ')
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
    body = response.read().decode('ISO-8859-1')
    response.close()
    connection.close()

    # Print http response
    print("%s %s" % (response.status, response.reason))
    for key, val in response.headers.items():
        print(colored(key, "cyan") + ": " + colored(val, "yellow"))
    if 'Content-Type' in response.headers:
        mimetype = response.headers['Content-Type'].split(';')[0]
        lexer = lexers.get_lexer_for_mimetype(mimetype)
        if 'application/json' in mimetype:
            body = json.dumps(json.loads(body), indent=4)
        colored_output = highlight(body, lexer, formatters.TerminalFormatter())
        print(colored_output)
    else:
        print(body)


if __name__ == '__main__':
    cli()
