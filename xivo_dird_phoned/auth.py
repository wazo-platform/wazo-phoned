# -*- coding: utf-8 -*-
# Copyright (C) 2015 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

import logging

from requests import RequestException
from threading import Timer

from xivo_auth_client import Client

logger = logging.getLogger(__name__)


class AuthClient(object):

    token_expiration = 6*60*60
    renew_time = int(0.8*token_expiration)
    renew_time_failed = 20

    def __init__(self, config, app_config):
        self.app_config = app_config
        self.app_config['token'] = None
        self.auth_client = Client(config['host'],
                                  port=config['port'],
                                  username=config['service_id'],
                                  password=config['service_key'],
                                  verify_certificate=config['verify_certificate'])

    def renew_token(self):
        logger.info('Renew service token')
        try:
            self.app_config['token'] = self.auth_client.token.new('xivo_service',
                                                                  expiration=self.token_expiration)['token']
        except RequestException as e:
            logger.exception(e)
            logger.warning('Create token with XiVO Auth failed. Reattempt in %d seconds', self.renew_time_failed)
            next_renew_time = self.renew_time_failed
        else:
            next_renew_time = self.renew_time
        finally:
            self._timer = Timer(next_renew_time, self.renew_token)
            self._timer.deamon = True
            self._timer.start()

    def stop(self):
        self._timer.cancel()
