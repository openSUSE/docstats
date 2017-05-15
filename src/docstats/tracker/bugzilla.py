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

import re

_BUGZILLA_REGEX = re.compile(r'(?P<bugtracker>bsc|bnc)\s?#(?P<id>\d{2,9})')


def bugzilla(text):
    # Just "normalize" the tracker thing to "bsc" as "bnc" is outdated
    for tracker, item in _BUGZILLA_REGEX.findall(text):
        yield 'bsc', item
