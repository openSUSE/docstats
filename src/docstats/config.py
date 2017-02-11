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


def geturls(config, sections=None):
    """Yields all URLs from a repository in a tuple of (section, url) unless the section doesn't have
       the url keyword or the url is empty, In this case nothing is yielded.

    :param config: a :class:`configparser.ConfigParser` instance
    :type config: :class:`configparser.ConfigParser`
    :param list sections: a list of sections which are searched for
    :rtype: None | []
    :return: yields a tuple in the format (section, URL)
    :rtype: generator
    """
    if not sections:
        sections = config.sections()

    for sec in sections:
        value = config.get(sec, 'url', fallback=None)
        if value:
            yield sec, value


def getbranchparts(string, stdbranch='develop'):
    """Generator: Yields its branch name and optional start/end dates from a string

    For example:
    >>> list(getbranchparts('name'))
    [('name', 'develop', '', '')]
    >>> list(getbranchparts('name maintenance/SLE12'))
    [('name', 'maintenance/SLE12', '', '')]
    >>> list(getbranchparts('name maintenance/SLE12   abc'))
    [('name', 'maintenance/SLE12', 'abc', '')]
    >>> list(getbranchparts('name maintenance/SLE12   abc..'))
    [('name', 'maintenance/SLE12', 'abc', '')]
    >>> list(getbranchparts('name maintenance/SLE12   ..abc'))
    [('name', 'maintenance/SLE12', '', 'abc')]
    >>> list(getbranchparts('name maintenance/SLE12   abc..def'))
    [('name', 'maintenance/SLE12', 'abc', 'def')]

    :param string: a string in the format "NAME BRANCHNAME [[START][..][END]]
    :return: a tuple in the form "(branchname, start, end)"; the start and end parts can be an empty string
    :rtype: generator
    """
    # Remove duplicated spaces
    data = ' '.join(string.strip().split()).split(' ')

    if len(data) == 1:
        yield data[0], stdbranch, '', ''
    elif len(data) == 2:
        yield data[0], data[1], '', ''
    else:
        name = data[0]
        branchname = data[1]
        data = data[2].split('..')
        if len(data) == 1:
            yield name, branchname, data[0], ''
        else:
            yield name, branchname, data[0], data[1]


def getbranches(branches):
    """Generator: Yields all "branches" from a specific section like this:

    [section]
    branches =
        nameA  branch/a  abc
        nameB  branch/b  ..def
        nameC  branch/c  cde..eff
        # branch/d

    :param branches: a string of the branches key from the config file or None
    :rtype: str | None | ''
    :return: yields a tuple in the format (branch, from, to)
    :rtype: generator
    """

    if not branches:
        raise StopIteration

    for branch in branches.strip().split("\n"):
        branch = branch.strip()
        # If line starts with a comment character ignore this line
        # and continue with next:
        if branch[0] in ('#', ';'):
            continue
        yield from getbranchparts(branch)
