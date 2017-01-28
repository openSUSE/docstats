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
import urllib.parse


__all__ = ('git_urlparse', 'tmpdir')


#: For parsing GitHub URLs
_BASE_REGEX = r'[\w\._-]'
_USER_REGEX = _BASE_REGEX
_SERVER_REGEX = _USER_REGEX
_DOMAIN_REGEX = _USER_REGEX
_REPO_REGEX = _USER_REGEX
_DOMAIN_REPO_REGEX = (r'(?P<domain>{domain}+)/'
                      r'(?P<repo>{repo}+)'
                      r''.format(domain=_DOMAIN_REGEX,
                                 repo=_REPO_REGEX,
                                 )
                      )
_GITURL_REGEX = re.compile(r'(?P<user>{user}+)@'
                        r'(?P<server>{server}+):'
                        r'{domainrepo}+'
                        r''.format(user=_USER_REGEX,
                                   server=_SERVER_REGEX,
                                   domainrepo=_DOMAIN_REPO_REGEX,
                                   )
                           )

_GITDOMAIN_REPO_REGEX = re.compile(_DOMAIN_REPO_REGEX)

#:


def urlparse(url):
    """Parse Git URL, either git@server:domain/repo.git or http://server/domain/repo

    :param url:
    :return:
    """
    if url.endswith('.git'):
        url = url[:-4]
    if url.startswith('git@'):
        return git_urlparse(url)
    else:
        return http_urlparse(url)


def http_urlparse(url):
    """Parse Git HTTP(S) URls

    :param url: The URL starting usually with http:// or https://
    :return:
    """
    pr = urllib.parse.urlparse(url)
    groupdict = {'user': None, 'server': pr.netloc}
    path = pr.path[:-4] if pr.path.endswith('.git') else pr.path

    match =_GITDOMAIN_REPO_REGEX.search(path)
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

    # Cuts off ".git" ending
    if url.endswith('.git'):
        url = url[:-4]
    match = _GITURL_REGEX.search(url)
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
    # TODO: use string.Template?
    for var in ('USER', 'LANG', 'HOSTNAME'):
        replaceable = os.environ.get(var, '')
        path = path.replace("${}".format(var), replaceable)
    return path
