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

"""
Logging setup
"""

import logging
import sys
# import logging.config
# from os import path

__all__ = ('log', 'loggit', 'setloglevel', 'LOGLEVELS',)

#: ``log`` is the object to use for all log events
logging.getLogger(__name__).addHandler(logging.NullHandler())
log = logging.getLogger(__name__)

#: load the logging configuration
# LOGGING_CONF = path.join(path.dirname(path.abspath(__file__)),'logging.ini')
# logging.config.fileConfig(LOGGING_CONF, disable_existing_loggers=False)


#: We don't want any messages from git.cmd, except warnings
loggit = logging.getLogger('git.cmd')
loggit.setLevel(logging.WARN)

_ch = logging.StreamHandler(sys.stderr)
_frmt = logging.Formatter('[%(levelname)s]: %(message)s', '%H:%M:%S')
_ch.setFormatter(_frmt)
log.setLevel(logging.DEBUG)
log.addHandler(_ch)


#: Dictionary: Log levels to map verbosity level to logging values
LOGLEVELS = {None: logging.NOTSET,  # 0
             0: logging.NOTSET,     # 0
             1: logging.INFO,       # 20
             2: logging.DEBUG,      # 10
             }


def setloglevel(verbose):  # pragma: no cover
    """Set log level according to verbose argument

    :param int verbose: verbose level to set
    """
    log.setLevel(LOGLEVELS.get(verbose, logging.DEBUG))
