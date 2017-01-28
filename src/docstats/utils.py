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


__all__ = ('findbugid', 'findcommits', 'git_urlparse', 'http_urlparse', 'tmpdir', 'urlparse',)


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
#: For parsing text with bug fix information
_BUGTRACKER_REGEXES = (
    # see https://help.github.com/articles/closing-issues-via-commit-messages/
    re.compile(r'(?P<github>fix(?:es|ed)?|'
               r'close[sd]?|'
               r'resolve[sd]?)'
               r'(?:\s+(?:for))?'
               r'\s?#(?P<id>\d{1,9})', re.IGNORECASE),
    # see https://en.opensuse.org/openSUSE:Creating_a_changes_file_(RPM)#Bug_fix.2C_feature_implementation
    # https://en.opensuse.org/openSUSE:Packaging_Patches_guidelines#Current_set_of_abbreviations
    re.compile(r'(?P<bugtracker>bsc|bnc|boo|[fF]ate|FATE)'
               r'\s?#(?P<id>\d{2,9})'),
    # CVE
    re.compile(r'(CVE)-(?P<cve>\d{4}-\d{4,7})'),
    #
)


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


def findbugid(text):
    """Find Bugzilla IDs, GitHub, Fate, and CVEs

    :param text: the text containing bug information IDs
    :return: a list of tuples of all found bug IDs; each item has the format (type, value)
    :rtype: list
    """

    def _github(m):
        # "normalize" the text part of the match
        return [(text.lower(), number) for text, number in m]

    def _bugtracker(m):
        # we reuse the function from _github which just make the text
        # lowercase
        return _github(m)

    def _cve(m):
        # don't change anything for CVE entries
        return m

    # Order must match the regexes in _BUGTRACKER_REGEXES
    functions = [_github, _bugtracker, _cve]

    result = [ ]
    # Iterate through all possible regexes and deliver a tuple of
    # (regex, func). The "func" part is used to "cleanup" the matching
    for regex, func in zip(_BUGTRACKER_REGEXES, functions):
        match = regex.findall(text)
        if match is not None:
            # cleanup
            result.extend(func(match))

    return result


def findcommits(text):
    """Find commit hashes in text

    :param text: the text with possible commit hashes
    :return: a list of all found commit hashes
    """
    _COMMIT_HASH_REGEX = re.compile(r'(?P<commit>[cC]ommit)?'
                                    r'\s?[#]?'
                                    r'\b(?P<id>[0-9a-f]{5,40})\b')
    match = _COMMIT_HASH_REGEX.findall(text)
    if match:
        return [(text if text else 'commit', number) for text, number in match]
    else:
        return []
