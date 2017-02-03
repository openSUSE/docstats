#
# Copyright (c) 2017 SUSE Linux GmbH
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA
#

from .cli import parsecli
from .config import parseconfig, geturls
from configparser import DuplicateSectionError, DuplicateOptionError
from .log import log, setloglevel
from .utils import gettmpdir
from .worker import work

import os


def main(cliargs=None):
    """Entry point for the application script

    :param list cliargs: Arguments to parse or None (=use sys.argv)
    :return: return codes from ``ERROR_CODES``
    """
    try:
        args = parsecli(cliargs)
        setloglevel(args['-v'])
        log.info(args)

        configfile = args['CONFIGFILE']
        files, config = parseconfig(configfile)

        # print(args)
        # print(config)
        # ----
        # print("Sections found:", config.sections())
        # print("branch", config['doc-slert']['branch'])
        # print("url", config['doc-slert']['url'])
        # ----
        basedir = gettmpdir(config.get('globals', 'tempdir', fallback=None))
        os.makedirs(basedir, exist_ok=True)
        work(config, basedir, sections=args['--sections'], jobs=args['--jobs'])

    except (DuplicateSectionError, DuplicateOptionError) as error:
        log.error(error)
        return 20

    except (FileNotFoundError, OSError) as error:
        log.error(error)  # exc_info=1
        return 10

    except KeyboardInterrupt:
        log.fatal("aborted.")
        return 10

    return 0
