wazo-phoned
================

[![Build Status](https://jenkins.wazo.community/buildStatus/icon?job=wazo-phoned)](https://jenkins.wazo.community/job/wazo-phoned)

wazo-phoned is a service to handle phone-related services using a simple REST API. Examples of
services are directory lookup using wazo-dird and the handling of BLFs.


## Translations

To extract new translations:

    % pybabel extract --mapping-file=wazo_phoned/babel.cfg --output-file=wazo_phoned/translations/messages.pot wazo_phoned

To create new translation catalog:

    % pybabel init -l <locale> --input-file=wazo_phoned/translations/messages.pot --output-dir=wazo_phoned/translations

To update existing translations catalog:

    % pybabel update --input-file=wazo_phoned/translations/messages.pot --output-dir=wazo_phoned/translations

Edit file `wazo_phoned/translations/<locale>/LC_MESSAGES/messages.po` and compile
using:

    % pybabel compile --directory=wazo_phoned/translations


### Generate .tx/config

    % tx set --auto-local -r wazo.wazo-phoned 'wazo_phoned/translations/<lang>/LC_MESSAGES/messages.po' --source-lang en --type PO --source-file wazo_phoned/messages.pot --execute


Docker
------

The wazoplatform/wazo-phoned image can be built using the following command:

    % docker build -t wazoplatform/wazo-phoned

The `wazoplatform/wazo-phoned` image contains a configuration file to listen to
HTTP requests on "0.0.0.0". To change this behavior, create or edit the file
`/etc/wazo-phoned/conf.d/listen.yml`


Running unit tests
------------------

```
apt-get install libpq-dev python-dev libffi-dev libyaml-dev
pip install tox
tox --recreate -e py39
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
