#!/usr/bin/env python3
# Copyright 2018-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from setuptools import setup
from setuptools import find_packages

setup(
    name='wazo-phoned',
    version='1.0',

    description='Wazo Directory Daemon',

    author='Wazo Authors',
    author_email='dev.wazo@gmail.com',

    url='http://wazo.community',

    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'wazo-phoned=wazo_phoned.bin.daemon:main',
        ],
    }
)
