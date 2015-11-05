# xivo-dird-phoned
[![Build Status](https://travis-ci.org/xivo-pbx/xivo-dird-phoned.png?branch=master)](https://travis-ci.org/xivo-pbx/xivo-dird-phoned)

xivo-dird-phoned is a service to authenticate phone to allow lookup on
xivo-dird with a phone using a simple REST API.


## Docker

The xivo/xivo-dird-phoned image can be built using the following command:

   % docker build -t xivo/xivo-dird-phoned .

The `xivo/xivo-dird-phoned` image contains a configuration file to listen to
HTTP requests on "0.0.0.0". To change this behavior, create or edit the file
`/etc/xivo-dird-phoned/conf.d/listen.yml`


## Testing

xivo-dird-phoned contains unittests and integration tests

### unittests

Dependencies to run the unittests are in the `requirements.txt` file.

    % pip install -r requirements.txt -r test-requirements.txt

To run the unittests

    % nosetests xivo_dird_phoned

### Integration tests

You need:

    - docker
    % pip install -r integration_tests/test-requirements.txt

A docker image named `dird-phoned-test` is required to execute the test suite.
To build this image execute:

    % cd integration_tests
    % make test-setup

`make test-setup` downloads a bunch of Docker images so it takes a long time,
but it only needs to be run when dependencies of xivo-dird-phoned change in any
way (new Python library, new server connection, etc.)

To execute the integration tests execute:

    % make test
