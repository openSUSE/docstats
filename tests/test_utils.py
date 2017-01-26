import pytest

from docstats.utils import git_urlparse


@pytest.mark.parametrize('url,expected', [
    #
    ('foo@', {}),
    #
    ('git@github.com:x/y.git', {'domain': 'x', 'repo': 'y', 'server': 'github.com'}),
    #

])
def test_git_urlparse(url, expected):
    assert git_urlparse(url) == expected