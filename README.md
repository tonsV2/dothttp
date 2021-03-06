# dothttp - Perform http requests defined in files
When developing a web app I often find myself keeping a file with a bunch of http/curl/wget commands which I use for testing.

Being able to define such HTTP requests in a simple readable format resembling the HTTP standard makes sense.

This could also be used for E2E or integration testing.

## File format
```
Method Request-URI
Header-field: Header-value
...
Request-Body
```

### Multiple requests
A file can contain multiple requests separated by three hash signs (###). Please see [examples/heads.http](examples/heads.http)

### Request-Body Shell Expressions 
Evaluate shell expressions in the request body using ```$(expression)```. Please see [examples/postman.http](examples/postman.http)

## Example
```
GET http://httpbin.org/
Connection: keep-alive
Accept: text/html
Accept-Language: en-US,en;q=0.9,es;q=0.8
```
Please see the [examples/](examples/) folder for more.

## Install
```bash
pip3 install dothttp
```

## Usage
```bash
dothttp examples/request.http
```
Or
```bash
dothttp examples/request.http examples/httpbin.http ...
```
Or
```bash
dothttp examples/*.http
```
Or
```bash
echo "GET https://www.google.com" | dothttp -
```

## Quirks/Notes
* Request URI needs to be absolute
* If the "Host" header is not set the hostname from the Request-URI is used

## Releases
*1.3.0*
- Request-Body Shell Expressions

*1.2.0*
- Multi request files

*1.1.0*
- Syntax highlighting of output

*1.0.1*
- Bug fix

*1.0.0*
- Initial release
