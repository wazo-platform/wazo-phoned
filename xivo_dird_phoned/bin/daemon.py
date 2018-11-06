# Copyright 2015-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import logging
import signal
import sys

from functools import partial
from xivo.daemonize import pidfile_context
from xivo.user_rights import change_user
from xivo.xivo_logging import setup_logging
from xivo_dird_phoned.controller import Controller
from xivo_dird_phoned.config import load as load_config

logger = logging.getLogger(__name__)


class _PreConfigLogger:

    class FlushableBuffer:

        def __init__(self):
            self._msg = []

        def info(self, msg, *args, **kwargs):
            self._msg.append((logging.INFO, msg, args, kwargs))

        def debug(self, msg, *args, **kwargs):
            self._msg.append((logging.DEBUG, msg, args, kwargs))

        def warning(self, msg, *args, **kwargs):
            self._msg.append((logging.WARNING, msg, args, kwargs))

        def critical(self, msg, *args, **kwargs):
            self._msg.append((logging.CRITICAL, msg, args, kwargs))

        def flush(self):
            for level, msg, args, kwargs in self._msg:
                logger.log(level, msg, *args, **kwargs)

    def __enter__(self):
        self._logger = self.FlushableBuffer()
        return self._logger

    def __exit__(self, _type, _value, _tb):
        self._logger.flush()


def main(argv=None):
    argv = argv or sys.argv[1:]
    with _PreConfigLogger() as logger:
        logger.debug('Starting xivo-dird-phoned')

        config = load_config(logger, argv)

        setup_logging(config['log_filename'], config['foreground'], config['debug'], config['log_level'])

    if config['user']:
        change_user(config['user'])

    controller = Controller(config)
    signal.signal(signal.SIGTERM, partial(sigterm, controller))

    with pidfile_context(config['pid_filename'], config['foreground']):
        controller.run()


def sigterm(controller, signum, frame):
    controller.stop(reason='SIGTERM')


if __name__ == '__main__':
    main(sys.argv[1:])
