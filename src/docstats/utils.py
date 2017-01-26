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

__all__ = ('git_urlparse', )

GITURL_RE = re.compile(r'git@(?P<server>[a-zA-Z\._]+):(?P<domain>\w+)/(?P<repo>\w+).git')


def git_urlparse(url):
    """Parse Git URLs

    :param str url: the Git(Hub) URL
    :return:
    """
    if not url.startswith('git@'):
        return {}
    match = GITURL_RE.search(url)
    if match is None:
        raise ValueError('Could not find any matching parts in your Git URL: %r' % url)
    return match.groupdict()
