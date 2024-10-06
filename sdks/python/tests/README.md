# Testing

This is only meant for developers to use for testing, DO NOT RUN IN A PRODUCTION ENVIRONMENT

Ensure that your environment has `pytest` and `pytest-asyncio` installed

`cd` to this directory
run `pytest`


you must have a file called `test.ini` file that looks like
```
[DEFAULT]
API_KEY = your_api_key
API_SECRET = your_api_secret
HOST = test_host
ACCOUNT = account_number
```