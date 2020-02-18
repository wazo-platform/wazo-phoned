# Copyright 2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import requests


class ConfdClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def url(self, *parts):
        return 'https://{host}:{port}/{path}'.format(
            host=self.host, port=self.port, path='/'.join(parts)
        )

    def is_up(self):
        url = self.url()
        try:
            response = requests.get(url, verify=False)
            return response.status_code == 404
        except requests.RequestException:
            return False

    def requests(self):
        url = self.url('_requests')
        return requests.get(url, verify=False).json()

    def reset(self):
        url = self.url('_reset')
        requests.post(url, verify=False)
