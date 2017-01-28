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
from .repo import analyze
from .utils import gettmpdir
from .worker import worker

import os


def main(cliargs=None):
    """Entry point for the application script

    :param list cliargs: Arguments to parse or None (=use sys.argv)
    :return: return codes from ``ERROR_CODES``
    """
    try:
        args = parsecli(cliargs)
        configfile = args['CONFIGFILE']
        files, config = parseconfig(configfile)
        print(args)
        print(config)
        # ----
        #print("Sections found:", config.sections())
        #print("branch", config['doc-slert']['branch'])
        #print("url", config['doc-slert']['url'])
        # ----
        tmpdir = gettmpdir(config.get('globals', 'tempdir', fallback=None))
        os.makedirs(tmpdir, exist_ok=True)
        queue = worker(geturls(config), tmpdir, jobs=args['--jobs'])
        analyze(queue, config)

    except (FileNotFoundError, OSError) as error:
        print(error)
        return 10

    except KeyboardInterrupt:
        print("aborted.")
        return 10

    return 0