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
#
# Module that contains the command line app.
#
# Why does this file exist, and why not put this in __main__?
#
#  You might be tempted to import things from __main__ later, but that will cause
#  problems: the code will get executed twice:
#
#  - When you run `python -mdocstats` python will execute
#    ``__main__.py`` as a script. That means there won't be any
#    ``docstats.__main__`` in ``sys.modules``.
#  - When you import __main__ it will get executed again (as a module) because
#    there's no ``docstats.__main__`` in ``sys.modules``.
#
#  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration


"""Create statistics of SUSE doc repositories

Usage:
   docstats [-h | --help]
   docstats [-v...] [options] CONFIGFILE

Options:
    -h, --help             Shows this help
    -v                     Raise verbosity level
    --jobs=N, -j N         Allow N jobs at once [default: 1]
    --sections=NAME, -s NAME
                           Select one or more sections from configuration file only (default all)
                           separated  by comma
    --version              Prints the version
    CONFIGFILE             The configuration file which contains all to repos to investigate
"""

from docopt import docopt, DocoptExit
import os


def parsecli(cliargs=None):
    """Parse CLI arguments with docopt

    :param list cliargs: List of commandline arguments
    :return: dictionary from docopt
    :rtype: dict
    """
    from docstats import __version__
    version = "%s %s" % (__package__, __version__)
    args = docopt(__doc__, argv=cliargs, version=version)

    checkcliargs(args)
    return args


def checkcliargs(args):
    """Make a consistency check

    :param args: dictionary from docopt
    :return: True | exceptions
    """

    configfile = args['CONFIGFILE']

    try:
        args['--jobs'] = int(args['--jobs'])
    except ValueError:
        raise DocoptExit("Option -j/--jobs does not contain a number")

    args['--sections'] = None if args['--sections'] is None else args['--sections'].split(',')

    if configfile is None:
        raise DocoptExit("Expected config file")

    if not os.path.exists(configfile):
        raise FileNotFoundError("Couldn't find {!r} config file.".format(configfile))
    return True
