#!/usr/bin/env python3
# Copyright 2018-2025 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from setuptools import find_packages, setup
from setuptools.command.build_py import build_py as _build_py

PROJECT = 'wazo-phoned'
AUTHOR = 'Wazo Authors'
EMAIL = 'dev@wazo.community'


class build_py(_build_py):
    def run(self):
        self.run_command('compile_catalog')
        super().run()


setup(
    name=PROJECT,
    version='1.0',
    description='Wazo Phone Daemon',
    author=AUTHOR,
    author_email=EMAIL,
    url='http://wazo-platform.org',
    packages=find_packages(),
    include_package_data=True,
    package_data={'wazo_phoned.plugins': ['*/api.yml']},
    setup_requires=['babel'],
    install_requires=['babel'],
    cmdclass={
        'build_py': build_py,
    },
    entry_points={
        'console_scripts': ['wazo-phoned=wazo_phoned.bin.daemon:main'],
        'wazo_phoned.plugins': [
            'api = wazo_phoned.plugins.api.plugin:Plugin',
            'blf = wazo_phoned.plugins.blf.plugin:Plugin',
            'aastra = wazo_phoned.plugins.aastra.plugin:Plugin',
            'cisco = wazo_phoned.plugins.cisco.plugin:Plugin',
            'config = wazo_phoned.plugins.config.plugin:Plugin',
            'endpoint = wazo_phoned.plugins.endpoint.plugin:Plugin',
            'fanvil = wazo_phoned.plugins.fanvil.plugin:Plugin',
            'gigaset = wazo_phoned.plugins.gigaset.plugin:Plugin',
            'htek = wazo_phoned.plugins.htek.plugin:Plugin',
            'polycom = wazo_phoned.plugins.polycom.plugin:Plugin',
            'snom = wazo_phoned.plugins.snom.plugin:Plugin',
            'status = wazo_phoned.plugins.status.plugin:Plugin',
            'thomson = wazo_phoned.plugins.thomson.plugin:Plugin',
            'yealink = wazo_phoned.plugins.yealink.plugin:Plugin',
        ],
    },
)
