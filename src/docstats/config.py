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


def geturls(config):
    """Yields all URLs from a repository; if a section doesn't have the url keyword it is skipped

    :param config: a :class:`configparser.ConfigParser` instance
    :type config: :class:`configparser.ConfigParser`
    :return: yields a tuple in the format (section, URL)
    :rtype: generator
    """
    for sec in config.sections():
        if config.get(sec, 'url', fallback=None) != '':
            yield sec, config[sec]['url']


def getbranchparts(string):
    """Generator: Yields its branch name and optional start/end dates from a string

    For example:
    >>> list(getbranch('maintenance/SLE12'))
    [('maintenance/SLE12', '', '')]
    >>> list(getbranch('maintenance/SLE12   abc'))
    [('maintenance/SLE12', 'abc', '')]
    >>> list(getbranch('maintenance/SLE12   abc..'))
    [('maintenance/SLE12', 'abc', '')]
    >>> list(getbranch('maintenance/SLE12   ..abc'))
    [('maintenance/SLE12', '', 'abc')]
    >>> list(getbranch('maintenance/SLE12   abc..def'))
    [('maintenance/SLE12', 'abc', 'def')]

    :param string: a string in the format "BRANCHNAME [[START][..][END]]
    :return: a tuple in the form "(branchname, start, end)"; the start and end parts can be an empty string
    :rtype: generator
    """
    # Remove duplicated spaces
    data = ' '.join(string.strip().split()).split(' ')

    if len(data) == 1:
        yield data[0], '', ''
    else:
        branchname = data[0]
        data = data[1].split('..')
        if len(data) == 1:
            yield branchname, data[0], ''
        else:
            yield branchname, data[0], data[1]


def getbranches(section, config):
    """Generator: Yields all "branches" from a specific section like this:

    [section]
    branches =
        branch/a  abc
        branch/b  ..def
        branch/c  cde..eff

    :param str section: the section
    :param config: a :class:`configparser.ConfigParser` instance
    :type config: :class:`configparser.ConfigParser`
    :return: yields a tuple in the format (branch, from, to)
    :rtype: generator
    """

    branches = config.get(section, 'branches', fallback=None)
    if branches is None:
        raise StopIteration

    for branch in branches.strip().split("\n"):
        yield from getbranchparts(branch)