xivo-dird-phoned
================

[![Build Status](https://travis-ci.org/xivo-pbx/xivo-dird-phoned.png?branch=master)](https://travis-ci.org/xivo-pbx/xivo-dird-phoned)

xivo-dird-phoned is a service to authenticate phone to allow lookup on
xivo-dird with a phone using a simple REST API.


Docker
------

The xivo/xivo-dird-phoned image can be built using the following command:

    % docker build -t wazopbx/xivo-dird-phoned

The `xivo/xivo-dird-phoned` image contains a configuration file to listen to
HTTP requests on "0.0.0.0". To change this behavior, create or edit the file
`/etc/xivo-dird-phoned/conf.d/listen.yml`


Running unit tests
------------------

```
apt-get install libpq-dev python-dev libffi-dev libyaml-dev
pip install tox
tox --recreate -e py27
```


Running integration tests
-------------------------

You need Docker installed.

```
cd integration_tests
pip install -U -r test-requirements.txt
make test-setup
make test
```
