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

from configparser import ConfigParser


def parseconfig(configfile):
    """Parses a INI docstats configuration file

    :param str configfile: path to INI file
    :return: instance of :class:`configparser.ConfigParser`

    Syntax of INI file:

    [globals]
    branch = develop

    [doc-sle]
    url = git@github.com:SUSE/doc-sle.git
    branch = develop
    # after =
    # before =

    There can be multiple sections (here: "doc-sle") which contains an URL, the name of the branch, and
    optional time ranges (before and after).
    """
    config = ConfigParser(default_section='globals')
    files = config.read(configfile)
    return files, config
