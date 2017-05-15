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

_FATE_REGEX = re.compile(r'(?:fate\s?#|https://fate\.suse\.com/)(\d+)', re.I)


def fate(text):
    """Searches for FATE entries in text, usually commit messages.

       It can detect:
       * FATE#123, fate#123, or Fate#123
       * https://fate.suse.com/123

    :param text: the text to investigate
    :return: yields "fate", item or an empty list
    """
    for item in _FATE_REGEX.findall(text):
        # the result will be, for example, either one of these:
        # tracker='fate#123', items=['fate', '123', '', '']
        #
        yield "fate", item
