# dothttp - Perform http requests defined in files
When developing a web app I often find myself keeping a file with a bunch of http/curl/wget commands which I use for testing.

Being able to define such HTTP requests in a simple readable format resembling the HTTP standard makes sense.

This could also be used for E2E or integration testing.

## File format
```
Method Request-URI
Header-field: Header-value
Request-Body
```

## Examples 
Please see the examples folder.

## Install
```bash
pip install dothttp
```

## Usage
```bash
dothttp examples/request.http
```

## Quirks/Notes
* Request URI needs to be absolute
* Host header will be overwritten
