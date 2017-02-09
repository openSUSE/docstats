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
   docstats [--version]
   docstats <command> [<args>...]

Options:
    -h, --help             Shows this help
    --version              Prints the version

The subcommands are:
   analyze, an      clone and analyze the repos found in the config file
   visualize, vis   visualize the result
"""

from docopt import docopt, DocoptExit
import os
from .config import parseconfig
from .utils import gettmpdir
from .worker import work
from textwrap import dedent


class AbstractCommand:
    """Base class for the commands"""

    def __init__(self, cmdargs, global_args):
        """Initialize the commands.

        :param cmdargs: arguments of the command
        :param global_args: arguments of the program
        """
        self.args = docopt(dedent(self.__doc__), argv=cmdargs)
        self.global_args = global_args
        self.checkargs()
        # print(">>> cmdargs:", cmdargs, global_args, self.args)

    def checkargs(self):
        try:
            self.args['--jobs'] =  int(self.global_args['--jobs'])
        except ValueError:
            raise DocoptExit("Option -j/--jobs does not contain a number")

    def execute(self):
        """Execute the commands"""
        raise NotImplementedError


class Analyze(AbstractCommand):
    """
    Clone and analyze the repos found in the config file

    Usage:
        analyze [-h | --help]
        analyze [-v...] [options] CONFIGFILE

    Abbreviation:
        an

    Options:
        -h, --help         Shows this help
        -v                 Raise verbosity level
        --sections=NAME, -s NAME
                           Select one or more sections from configuration file only (default all)
                           separated  by comma
        CONFIGFILE         The configuration file which contains all to repos to investigate
    """
    abbrev = "an"
    config = None

    def execute(self):
        print('>>> {}: globals={}, args={}'.format(self.__class__.__name__.lower(),
                              self.global_args,
                              self.args))
        configfile = self.args['CONFIGFILE']
        _, self.config = parseconfig(configfile)
        basedir = gettmpdir(self.config.get('globals', 'tempdir', fallback=None))
        os.makedirs(basedir, exist_ok=True)
        work(self.config, basedir, sections=self.args['--sections'], jobs=self.args['--jobs'])



class Visualize(AbstractCommand):
    """
    Visualize the result

    Usage:
       visualize [-h | --help]
       visualize [-v...] [options] JSONFILE

    Abbreviation:
       vis

    Options:
       -h, --help   Shows this help
       -v           Raise verbosity level
       JSONFILE     The JSON file from the 'analyze' step
    """
    abbrev = 'vis'

    def execute(self):
        print('{}: globals={}, args={}'.format(self.__class__.__name__,
                                               self.global_args,
                                               self.args))


def parsecli(cliargs=None):
    """Parse CLI arguments with docopt

    :param list cliargs: List of commandline arguments
    :return: dictionary from docopt
    :rtype: dict
    """
    from docstats import __version__
    version = "%s %s" % (__package__, __version__)
    args = docopt(__doc__, argv=cliargs, version=version, options_first=True)

    cmdname = args.pop('<command>')
    cmdargs = args.pop('<args>')
    commandlist = [Analyze, Visualize]
    commands = {}

    for cls in commandlist:
        commands[cls.__name__.lower()] = cls
        commands[cls.abbrev] = cls
    print(">>>", commands, cmdname)

    if cmdargs is None:
        cmdargs = {}

    # After 'poping' '<command>' and '<args>', what is left in the args dictionary are the global arguments.
    # Retrieve the class from the 'commands' module.
    try:
        cmdclass = commands[cmdname]
    except AttributeError:
        raise DocoptExit('Unknown command %r' % cmdname)

    # Create an instance of the command.
    cmd = cmdclass(cmdargs, args)

    # Execute the command.
    cmd.execute()

    # checkcliargs(args)
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
