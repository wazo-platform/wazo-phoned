#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools import find_packages

setup(
    name='xivo-dird-phoned',
    version='1.0',

    description='XiVO Directory Daemon',

    author='Avencall',
    author_email='dev@avencall.com',

    url='https://github.com/xivo-pbx/xivo-dird-phoned',

    packages=find_packages(),

    scripts=['bin/xivo-dird-phoned']
)
