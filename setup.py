#!/usr/bin/env python3
# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

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
    entry_points={
        'console_scripts': [
            'xivo-dird-phoned=xivo_dird_phoned.bin.daemon:main',
        ],
    }
)
