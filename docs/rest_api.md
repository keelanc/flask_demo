# REST API

## REST API version
TBD (Future work: Endpoints should be preceded by a version number. Example, http://localhost:5000/api/v1/command)  
URIs are relative to http://localhost:5000, unless otherwise noted.

## HTTP Headers
To make a request with JSON, the appropriate headers are:
```
Content-Type: application/json
Accept: application/json
```

## Send a command
Send a command to be executed by the server shell.

| URI      | HTTP Method |
| -------- | ----------- |
| /command | PUT |
| | |

### Request Body
```json
{
    "command": "echo foo"
}
```

### Response
Status: 200
```json
{
  "status": 0,
  "stderr": "",
  "stdout": "foo\n"
}
```
