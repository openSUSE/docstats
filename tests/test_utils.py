import pytest
from unittest.mock import patch

from docstats.utils import git_urlparse, http_urlparse, gettmpdir, urlparse


@pytest.mark.parametrize('url,expected', [
    #
    ('git@Foo-bar.com:X-Z/A-b.git', {'domain': 'X-Z', 'repo': 'A-b', 'server': 'Foo-bar.com', 'user': 'git'}),
    #
    ('http://github.com/X/Y',
     {'domain': 'X', 'repo': 'Y', 'server': 'github.com', 'user': None}),
])
def test_urlparse(url, expected):
    assert urlparse(url) == expected


# Matches any URL with USER@SERVER:DOMAIN/REPO.git
@pytest.mark.parametrize('url,expected', [
    #
    ('git@github.com:x/y.git', {'domain': 'x', 'repo': 'y', 'server': 'github.com', 'user': 'git'}),
    #
    ('git@github.com:x/a-b.git', {'domain': 'x', 'repo': 'a-b', 'server': 'github.com', 'user': 'git'}),
    #
    ('git@github.com:X/A-b.git', {'domain': 'X', 'repo': 'A-b', 'server': 'github.com', 'user': 'git'}),
    #
    ('git@Foo-bar.com:X-Z/A-b.git', {'domain': 'X-Z', 'repo': 'A-b', 'server': 'Foo-bar.com', 'user': 'git'}),
    #
    pytest.mark.xfail(('foo@', {}),),
    #
    pytest.mark.xfail(('git@x', {} )),
    #
])
def test_git_urlparse(url, expected):
    assert git_urlparse(url) == expected


@pytest.mark.parametrize('url,expected', [
    #
    ('http://github.com/X/Y.git',
     {'domain': 'X', 'repo': 'Y', 'server': 'github.com', 'user': None}),
    #
    ('https://github.com/X/Y.git',
     {'domain': 'X', 'repo': 'Y', 'server': 'github.com', 'user': None}),
    #
    ('ftp://github.com/X/Y.git',
     {'domain': 'X', 'repo': 'Y', 'server': 'github.com', 'user': None}),
    #
    ('http://github.com/X/Y',
     {'domain': 'X', 'repo': 'Y', 'server': 'github.com', 'user': None}),
    #
    pytest.mark.xfail(('http://github.com', {} )),
    #
    # pytest.mark.xfail(('http://github.com/A/B', {} )),
])
def test_http_urlparse(url, expected):
    assert http_urlparse(url) == expected


@pytest.mark.parametrize('path,expected', [
    ('foo',                       'foo'),
    ('foo-$NOT_THERE',            'foo-$NOT_THERE'),
    ('foo-$USER',                 'foo-tux'),
    ('foo-$HOSTNAME',             'foo-myhost'),
    ('foo-$LANG',                 'foo-en'),
    ('foo-$USER-$LANG',           'foo-tux-en'),
    ('foo-$USER-$LANG-$HOSTNAME', 'foo-tux-en-myhost'),

])
def test_tmpdir(path, expected):
    with patch.dict('os.environ', {'HOSTNAME': 'myhost', 'USER': 'tux', 'LANG': 'en'}):
        assert gettmpdir(path) == expected