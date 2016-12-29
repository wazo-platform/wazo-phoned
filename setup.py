#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools import find_packages

setup(
    name='xivo-dird-phoned',
    version='1.0',

    description='XiVO Directory Daemon',

    author='Wazo Authors',
    author_email='dev.wazo@gmail.com',

    url='http://wazo.community',

    packages=find_packages(),

    scripts=['bin/xivo-dird-phoned']
)
