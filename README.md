wazo-phoned
================

[![Build Status](https://jenkins.wazo.community/buildStatus/icon?job=wazo-phoned)](https://jenkins.wazo.community/job/wazo-phoned)

wazo-phoned is a service to authenticate phone to allow lookup on
wazo-dird with a phone using a simple REST API.


Docker
------

The wazopbx/wazo-phoned image can be built using the following command:

    % docker build -t wazopbx/wazo-phoned

The `wazopbx/wazo-phoned` image contains a configuration file to listen to
HTTP requests on "0.0.0.0". To change this behavior, create or edit the file
`/etc/wazo-phoned/conf.d/listen.yml`


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
