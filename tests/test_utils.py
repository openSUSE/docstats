import pytest
from unittest.mock import patch

from docstats.utils import (compare_usernames,
                            git_urlparse,
                            http_urlparse,
                            gettmpdir,
                            urlparse,
                            findallmails,
                            findbugid,
                            findcommits,
                            )


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


@pytest.mark.parametrize('text,expected', [
    #
    ('normal text',   []),
    #
    ('text with 123,', []),
    #
    (" fix #123 ", [('fix', '123')]),
    #
    (" fixes #123! ", [('fixes', '123')]),
    #
    (" Fixed #123: ", [('fixed', '123')]),
    #
    (" close #123 ", [('close', '123')]),
    #
    (" closes #123 ", [('closes', '123')]),
    #
    (" closed #123 ", [('closed', '123')]),
    #
    (" resolve #123 ", [('resolve', '123')]),
    #
    (" resolves #123 ", [('resolves', '123')]),
    #
    (" resolved #123 ", [('resolved', '123')]),
    #
    ('and this fixes #123!', [('fixes', '123')]),
    #
    ('had fixed #123!', [('fixed', '123')]),
    # Multiple cases
    (" close #123, closes #345 ", [('close', '123'), ('closes', '345')]),
    # Special case "fix for #..."
    (" fix for #123 ", [('fix', '123')]),

])
def test_findbugid_github(text, expected):
    # Just for GitHub issues
    assert findbugid(text) == expected



@pytest.mark.parametrize('text,expected', [
    #
    ('the quick brown fox', []),
    #
    ('Closes tux/example_repo#76', [('closes', 'tux', 'example_repo', '76')]),
    #
    ('Closes Tux/Example_Repo#76', [('closes', 'tux', 'example_repo', '76')]),
])
def test_findbugid_extern_github(text, expected):
    # Just for GitHub issues
    assert findbugid(text) == expected


@pytest.mark.parametrize('text,expected', [
    #
    ('the quick brown fox', []),
    # For different bugtracker issues
    ('bsc#12345', [('bsc', '12345')]),
    #
    ('bnc#12345', [('bnc', '12345')]),
    #
    ('bnc #12345', [('bnc', '12345')]),
    #
    ('fix bnc#12345', [('bnc', '12345')]),
    #
    ('see bsc#123, bsc #345, and bsc#5678', [('bsc', '123'), ('bsc', '345'), ('bsc', '5678')]),
    #
    ('see Fate#123, FATE#345, and fate#5678', [('fate', '123'), ('fate', '345'), ('fate', '5678')]),
])
def test_findbugid_bugtracker(text, expected):

    assert findbugid(text) == expected


@pytest.mark.parametrize('text,expected', [
    #
    ('the quick brown fox', []),
    #
    ('CVE-2017-1234', [('CVE', '2017-1234')]),
    #
])
def test_findbugid_cve(text, expected):
    # Common Vulnerabilities and Exposures(CVE)
    assert findbugid(text) == expected


@pytest.mark.parametrize('text,expected', [
    #
    ('the quick brown fox', []),
    #
    ('commit de9ddf8', [('commit', 'de9ddf8')]),
    #
    ('commit #de9ddf8', [('commit', 'de9ddf8')]),
    #
    ('#de9ddf8', [('commit', 'de9ddf8')]),
    #
    ('de9ddf8, abede', [('commit', 'de9ddf8'), ('commit', 'abede')]),
    #
    ('abcdf, x123, 345', [('commit', 'abcdf')]),
    # Hmn... should we remove this as a possible commit?
    ('the deadfeed, ', [('commit', 'deadfeed')]),
])
def test_findcommits(text, expected):
    assert findcommits(text) == expected


@pytest.mark.parametrize('email,other,expected', [
    # If both strings are the same
    ("Tux Penguin <scholle@greenland.ice>",
     "Tux Penguin <scholle@greenland.ice>", True),
    # Both names are equal, but not email:
    ("Tux Penguin <scholle@greenland.ice>",
     "Tux Penguin <info@example.org>", True),
    # Both names are not equal, but email:
    ("Tux <tux@greenland.ice>",
     "Tux Penguin <tux@greenland.ice>", True),
    # With umlauts
    ("Jürgen  <js@example.org>",
     "Jürgen Beispiel  <js@example.org>", True),
    # Both names and email addresses are different:
    ("Tux Penguin <tux@greenland.ice>",
     "Wilber Gimp <wilber@gimp.org>", False),
    # First name missing the email address:
    ("Tux Penguin",
     "Wilber Gimp <wilber@gimp.org>", False),
    # Second name missing the email address:
    ("Tux Penguin <tux@greenland.ice>",
     "Wilber Gimp", False),
    # Email address without brackets
    ("Tux Penguin tux@greenland.ice",
     "Wilber Gimp wilber@gimp.org", False),

])
def test_compare_usernames(email, other, expected):
    assert compare_usernames(email, other) == expected


@pytest.mark.parametrize('text,expected', [
    # Empty text
    ("", []),
    #
    (None, []),
    #
    ("tux@penguin.com", ['tux@penguin.com']),
    #
    ("tux@penguin.com tuxine@penguin.com", ['tux@penguin.com', 'tuxine@penguin.com']),
    #
    ("tux@penguin.com, tuxine@penguin.com", ['tux@penguin.com', 'tuxine@penguin.com']),
    #
    ("tux@penguin.com,tuxine@penguin.com", ['tux@penguin.com', 'tuxine@penguin.com']),
    #
    ("aa@aa.com,bb@bb.com,cc@cc.com", ['aa@aa.com', 'bb@bb.com', 'cc@cc.com']),
])
def test_findallmails(text, expected):
    assert findallmails(text) == expected