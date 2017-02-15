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

from .bugzilla import bugzilla
from .github import github
from .trello import trello
from .fate import fate

TRACKERS = ('fate', 'bsc', 'gh', 'trello')
TRACKER_FUNCS =  (fate, bugzilla, github, trello)


def findbugid(text):
    """Find Bugzilla IDs, GitHub, Fate, and CVEs

    :param text: the text containing bug information IDs
    :return: a list of tuples of all found bug IDs; each item has the format (type, value)
    :rtype: list
    """
    for func in TRACKER_FUNCS:
        yield from func(text)
