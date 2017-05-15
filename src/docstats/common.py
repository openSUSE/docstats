#
# Copyright (c) 2017 SUSE Linux GmbH
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of version 3 of the GNU General Public License as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, contact SUSE LLC.
#
# To contact SUSE about this file by physical or electronic mail,
# you may find current contact information at www.suse.com

from logging import (BASIC_FORMAT,
                     CRITICAL,
                     DEBUG,
                     FATAL,
                     ERROR,
                     INFO,
                     NOTSET,
                     WARN,
                     WARNING,
                     )


#: Map verbosity to log levels
LOGLEVELS = {None: WARNING,  # 0
             0: WARNING,
             1: INFO,
             2: DEBUG,
             }


DEBUG_FORMAT = "[%(levelname)s] %(name)s:%(lineno)s %(message)s"
# SIMPLE_FORMAT = "%(levelname)s:%(name)s:%(message)s"

#: Default logging dict for :class:`logging.config.dictConfig`:
DEFAULT_LOGGING_DICT = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '[%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'NOTSET',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            # 'stream': 'ext://sys.stderr',
        },
    },
    'loggers': {
        'docstats': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': True
        },
        # We don't want any messages from git.cmd, except warnings
        'git.cmd': {
            'handlers': ['default'],
            'level': 'WARNING',
            'propagate': True,
        },
    }
}
