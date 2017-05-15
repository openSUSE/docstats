#

import pytest
from unittest.mock import patch

#from docstats.utils import (compare_usernames,
#                            git_urlparse,
#                            http_urlparse,
#                            gettmpdir,
#                            urlparse,
#                            findallmails,
#                            # findbugid,
#                            findcommits,
#                            )

from docstats.tracker.github import github
from docstats.tracker.fate import fate
from docstats.tracker.trello import trello
from docstats.tracker.bugzilla import bugzilla




@pytest.mark.parametrize('text,expected', [
    #
    ('normal text',   []),
    #
    ('text with 123,', []),
    #
    (" fix #123 ", [('gh', '123')]),
    #
    (" fixes #123! ", [('gh', '123')]),
    #
    (" Fixed #123: ", [('gh', '123')]),
    #
    (" close #123 ", [('gh', '123')]),
    #
    (" closes #123 ", [('gh', '123')]),
    #
    (" closed #123 ", [('gh', '123')]),
    #
    (" resolve #123 ", [('gh', '123')]),
    #
    (" resolves #123 ", [('gh', '123')]),
    #
    (" resolved #123 ", [('gh', '123')]),
    #
    ('and this fixes #123!', [('gh', '123')]),
    #
    ('had fixed #123!', [('gh', '123')]),
    # Multiple cases
    (" close #123, closes #345 ", [('gh', '123'), ('gh', '345')]),
    # Special case "fix for #..."
    (" fix for #123 ", [('gh', '123')]), #

])
def test_github(text, expected):
    # Just for GitHub issues
    assert list(github(text)) == expected



@pytest.mark.parametrize('text,expected', [
    #
    ('the quick brown fox', []),
    #
    ('Closes tux/example_repo#76', [('closes', 'tux', 'example_repo', '76')]),
    #
    ('Closes Tux/Example_Repo#76', [('closes', 'tux', 'example_repo', '76')]),
])
def _test_github_different_repos(text, expected):
    assert list(github(text)) == expected


@pytest.mark.parametrize('text,expected', [
    #
    ('the quick brown fox', []),
    # For different bugtracker issues
    ('bsc#12345', [('bsc', '12345')]),
    #
    ('bnc#12345', [('bsc', '12345')]),
    #
    ('bnc #12345', [('bsc', '12345')]),
    #
    ('fix bnc#12345', [('bsc', '12345')]),
    #
    ('see bsc#123, bsc #345, and bsc#5678', [('bsc', '123'), ('bsc', '345'), ('bsc', '5678')]),
    #
])
def test_bugzilla(text, expected):
    assert list(bugzilla(text)) == expected


@pytest.mark.parametrize('text,expected', [
    #
    ('the quick brown fox', []),
    # For different bugtracker issues
    ('trello#12345', [('trello', '12345')]),
    #
    ('Trello#12345', [('trello', '12345')]),
    #
    ('Trello #12345', [('trello', '12345')]),
    #
    ('fix trello#12345', [('trello', '12345')]),
    #
    ('see trello#123, Trello #345, and TRELLO#5678',
     [('trello', '123'), ('trello', '345'), ('trello', '5678')]),
    # This is pointing to a board; we don't want this as in our result
    ('Fix trello#123 and https://trello.com/b/cjXBA50P/sle-12-sp2',
     [('trello', '123'),]),
    # This is pointing to a card; we want this:
    ('Fix trello#123 and https://trello.com/c/V9Y2u46g',
     [('trello', '123'), ('trello', 'V9Y2u46g')]),
])
def test_trello(text, expected):

    assert list(trello(text)) == expected


@pytest.mark.parametrize('text,expected', [
    #
    ('the quick brown fox', []),
    #
    ('fate#123', [('fate', '123')]),
    #
    ('Fate#12345', [('fate', '12345')]),
    #
    ('FATE#12345', [('fate', '12345')]),
    #
    ('see fate#123, Fate #345, and FATE#5678',
     [('fate', '123'), ('fate', '345'), ('fate', '5678')]),
    #
    ('Fix fate#123 and https://fate.suse.com/3456',
     [('fate', '123'), ('fate', '3456')]),
])
def test_fate(text, expected):
    assert list(fate(text)) == expected
