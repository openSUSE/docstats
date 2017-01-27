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
import os
from urllib.parse import urlparse


__all__ = ('git_urlparse', 'tmpdir')


_GITURL_RE = re.compile(r'(?P<user>[\w\._-]+)@'
                        r'(?P<server>[\w\._-]+):'
                        r'(?P<domain>[\w\._-]+)/'
                        r'(?P<repo>[\w\._-]+)\.git')
_GITDOMAIN_REPO_RE = re.compile(r'(?P<domain>[\w\._-]+)/(?P<repo>[\w_-]+)')


def http_urlparse(url):
    """

def http_urlparse(url):
    """Parse Git HTTP(S) URls

    :param url:
    :return:
    """
    pr = urlparse(url)
    groupdict = {'user': None, 'server': pr.netloc}
    match =_GITDOMAIN_REPO_RE.search(pr.path)
    if match is None:
        # this should not happen...
        raise ValueError('Could not find any matching parts in your Git URL: %r' % url)
    groupdict.update(match.groupdict())
    return groupdict


def git_urlparse(url):
    """Parse Git URLs

    :param str url: the Git(Hub) URL
    :return: a dict; if you pass the url "git@github.com:x/y.git" you will get the content
            {'domain': 'x', 'repo': 'y', 'server': 'github.com'}
    """
    # HINT: Unfortunately, urllib.parse.urlparse cannot be used :-( therefore we use regexes:
    # >>> urllib.parse.urlparse('git@github.com:x/y.git')
    # ParseResult(scheme='', netloc='', path='git@github.com:x/y.git', params='', query='', fragment='')
    match = _GITURL_RE.search(url)
    if match is None:
        # this should not happen...
        raise ValueError('Could not find any matching parts in your Git URL: %r' % url)
    return match.groupdict()


def gettmpdir(path):
    """Constructs the string of a temporary path and replaces any variables in this string

    For example, if you have "/tmp/foo-$USER" and the current user is "tux", then it will return
    "/tmp/foo-tux"

    Current supported variables are: USER, LANG, HOSTNAME
    If an environment variable is not set, it will evaluate to an empty string.

    :param path: a path with or without any "shell" variables
    :return: the replaced string
    :rtype: str
    """
    for var in ('USER', 'LANG', 'HOSTNAME'):
        replaceable = os.environ.get(var, '')
        path = path.replace("${}".format(var), replaceable)
    return path