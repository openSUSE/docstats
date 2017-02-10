#

import git
import pytest
import sys

from docstats.repo import (cleanup_dict,
                           if_range_is_empty,
                           collect_committers,
                           collect_diffstats,
                           collect_issues,
                           iter_commits,
                           init_stats_dict,
                           init_tracker_dict,
                           init_committer_dict,
                           )
from docstats.utils import TRACKERS
from unittest.mock import patch, MagicMock, Mock, PropertyMock


skip_below_py345 = pytest.mark.skipif((sys.version_info.major,
                                       sys.version_info.minor,
                                       sys.version_info.micro) < (3, 4, 5),
                               reason="skip test for python3.4.x")


# This is going to fail for 3.4.2 with the following error message:
# pytest.fixture functions cannot use ``yield``. Instead write and return an inner
# function/generator and let the consumer call and iterate over it.
#
#@skip_below_py345
#def test_repo(gitrepo):
#    print("Git-Repo:", gitrepo)


def test_init_committer_dict():
    resultdict = init_committer_dict()
    assert len(resultdict) == 4
    assert not all(resultdict.values())


def test_init_tracker_dict():
    resultdict = init_tracker_dict()
    assert len(TRACKERS) == len(resultdict)
    assert not all(resultdict.values())


def test_init_stats_dict():
    resultdict = init_stats_dict()
    assert not all(resultdict.values())


@patch('docstats.worker.git.Repo')
def test_if_range_is_empty_with_False(mock_repo):
    def yield_empty():
        yield iter([])

    mock_repo.iter_commits.side_effect = yield_empty()
    assert not if_range_is_empty(mock_repo, '')


@patch('docstats.worker.git.Repo')
def test_if_range_is_empty_with_True(mock_repo):
    def yield_commit():
        yield iter(['fake-commit'])

    mock_repo.iter_commits.side_effect = yield_commit()
    assert  if_range_is_empty(mock_repo, '')


@pytest.mark.parametrize('user,expected', [
    #
    (git.Actor('Tux Penguin', 'tux@example.org'),
     {'team-committers': ['tux@example.org'],
      'team-committers-mails': ['tux@example.org'],
      'external-committers': [],
      'external-committers-mails': []}),
    #
    (git.Actor('Wilber Gimp', 'wilber@example.net'),
     {'team-committers': [],
      'team-committers-mails': [],
      'external-committers': ['wilber@example.net'],
      'external-committers-mails': ['wilber@example.net']}
    ),
])
def test_collect_committers(user, expected):
    binsha = b'\x12' * 20
    commit = git.Commit('fake-repo', binsha,
                        author=user, committer=user,
                        message="fake commit message")
    dictresult = {'team-committers': [], 'team-committers-mails': [],
                  'external-committers': [], 'external-committers-mails': []}
    collect_committers(commit, dictresult,
                       {'tux@example.org': 'tux@example.org',
                       })
    assert dictresult == expected


def test_collect_diffstats():
    dictresult = init_stats_dict()
    stats = {'deletions': 1, 'files': 1, 'insertions': 1, 'lines': 2}
    # See https://docs.python.org/3/library/unittest.mock.html#unittest.mock.PropertyMock
    mock_commit = MagicMock(spec=git.Commit)
    p = PropertyMock(return_value=stats)
    type(mock_commit.stats).total = p
    collect_diffstats(mock_commit, dictresult)
    assert dictresult == stats


@pytest.mark.parametrize('msg,expected', [
    #
    ("Fix bnc#1234, bnc#2345",
     {'bnc': ['1234', '2345']}),
    #
    ('Fix #123', {'gh': ['123']}),
    #
    ('fix #123', {'gh': ['123']}),
    #
    ('Fixes #123', {'gh': ['123']}),
    #
    ('Fixed #123', {'gh': ['123']}),
    #
    ('Close #123', {'gh': ['123']}),
    #
    ('close #123', {'gh': ['123']}),
    #
    ('closes #123', {'gh': ['123']}),
    #
    ('closed #123', {'gh': ['123']}),
    #
    ('Resolves #123', {'gh': ['123']}),
])
def test_collect_issues(msg, expected):
    dictresult = init_tracker_dict().copy()
    collect_issues(msg, dictresult)
    diffkeys = expected.keys() & dictresult.keys()

    for key in diffkeys:
        assert dictresult[key] == expected[key]


# @patch('docstats.repo.configparser.ConfigParser')
def test_iter_commits():
    # iter_commits(config, repo, dictresult, name, branchname, start=None, end=None)

    def iter_commits(rev):
        yield "first commit"
        yield "second commit"

    # Initialize the result dictionary with default values:
    name = "foo"
    branchname = "develop"
    dictresult = {}
    start = end = None
    dictresult[name] = {}
    dictresult[name]['branch'] = branchname
    dictresult[name]['start'] = str(start)
    dictresult[name]['end'] = str(end)
    dictresult = init_tracker_dict().copy()
    dictresult.update(init_stats_dict())
    dictresult.update(init_committer_dict())

    # Mock configparser.ConfigParser
    mock_config = Mock()
    mock_config.defaults.return_value = {}  # team members mail

    # Mock repository
    mock_repo = Mock()
    mock_repo.iter_commits.side_effects = iter_commits
    mock_repo.git.checkout.return_value = None

    #result = iter_commits(mock_config,
    #                      mock_repo,
    #                      dictresult,
    #                      name,
    #                      branchname,
    #                      # start=start,
    #                      # end=end
    #                      )
    #assert result


def test_cleanup_dict():
    #
    teams =  ('team-committers', 'external-committers',
              # These are just for debugging purposes:
              'team-committers-mails', 'external-committers-mails')
    resultdict = {}
    resultdict['A'] = init_tracker_dict()
    resultdict['A']['bnc'].extend(['123', '123'])

    for item in teams:
        resultdict['A'][item] = ['a', 'a', 'b']

    cleanup_dict(resultdict)
    assert len(resultdict['A']['bnc']) == 1
    for item in teams:
        assert resultdict['A'][item] == 2
