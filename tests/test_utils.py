import pytest
from unittest.mock import patch

from docstats.utils import git_urlparse, gettmpdir


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