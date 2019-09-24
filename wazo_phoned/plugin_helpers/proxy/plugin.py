# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from abc import ABCMeta, abstractmethod


class ProxyPlugin(metaclass=ABCMeta):

    menu_url = '/directories/menu/<profile>/{vendor}'
    input_url = '/directories/input/<profile>/{vendor}'
    lookup_url = '/directories/lookup/<profile>/{vendor}'
    vendor = None

    def load(self, dependencies):
        api = dependencies['api']
        dird_config = dependencies['config']['dird']
        class_kwargs = {
            'vendor': self.vendor,
            'dird_host': dird_config['host'],
            'dird_port': dird_config['port'],
            'dird_verify_certificate': dird_config.get('verify_certificate', True),
        }

        self.menu_url = self.menu_url.format(vendor=self.vendor)
        self.input_url = self.input_url.format(vendor=self.vendor)
        self.lookup_url = self.lookup_url.format(vendor=self.vendor)
        self._add_resources(api, class_kwargs)

    @abstractmethod
    def _add_resources(self, api, class_kwargs):
        pass
