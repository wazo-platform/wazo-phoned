wazo-phoned
================

[![Build Status](https://jenkins.wazo.community/buildStatus/icon?job=wazo-phoned)](https://jenkins.wazo.community/job/wazo-phoned)

wazo-phoned is a service to authenticate phone to allow lookup on
wazo-dird with a phone using a simple REST API.


## Translations

To extract new translations:

    % pybabel extract --mapping-file=wazo_phoned/babel.cfg --output-file=wazo_phoned/translations/messages.pot wazo_phoned

To create new translation catalog:

    % pybabel init -l <locale> --input-file=wazo_phoned/translations/messages.pot --output-dir=wazo_phoned/translations

To update existing translations catalog:

    % pybabel update --input-file=wazo_dird/messages.pot --output-dir=wazo_dird/translations

Edit file `wazo_phoned/translations/<locale>/LC_MESSAGES/messages.po` and compile
using:

    % pybabel compile --directory=wazo_phoned/translations


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
