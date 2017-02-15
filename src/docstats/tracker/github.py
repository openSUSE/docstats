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


#: For parsing GitHub URLs
_BASE_REGEX = r'[\w\._-]'
_USER_REGEX = _BASE_REGEX
_SERVER_REGEX = _USER_REGEX
_DOMAIN_REGEX = _USER_REGEX
_REPO_REGEX = _USER_REGEX
_DOMAIN_REPO_REGEX = (r'(?:(?P<domain>{domain}+)/'
                     r'(?P<repo>{repo}+))?'
                     r''.format(domain=_DOMAIN_REGEX,
                                repo=_REPO_REGEX,
                                ))


# see https://help.github.com/articles/closing-issues-via-commit-messages/
# external GitHub repositories
_GH_REGEX = re.compile(r'(?P<github>fix(?:es|ed)?\s(?:for)?|'
                       r'close[sd]?|'
                       r'resolve[sd]?)'
                       r'\s?'
                       r'%s#(?P<id>\d{1,9})' % _DOMAIN_REPO_REGEX,
                       re.I)

def github(text):
    # yield from _GH_REGEX.findall(text)
    for action, *item in _GH_REGEX.findall(text):
        #if action.lower() in ('clo', 'fix', 'res'):
        #    key = 'gh'
        #else:
        #    key = 'gh*'
        key = 'gh'
        if item[1]:
            yield (key, "{}/{}#".format(*item))
        else:
            yield key, item[-1]