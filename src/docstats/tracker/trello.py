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

_TRELLO_REGEX = re.compile(r'(?:trello\s?#|https://trello\.com/c/)(\d+|\w{8})\b', re.I)


def trello(text):
    """Searches for Trello entries in text, usually commit messages.

       It can detect:
       * Trello#123, trello#123, or trello#123
       * https://trello.com/c/123 and https://trello.com/c/123/long-title
         would lead to the same Trello number (here: 123)

       Board URLs starting with https://trello.com/b/... are not included in the result.

    :param text: the text to investigate
    :return: yields "fate", item or an empty list
    """
    for item in _TRELLO_REGEX.findall(text):
        yield 'trello', item
