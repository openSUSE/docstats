#

import pytest
import py
import sys

from docstats.repo import if_range_is_empty
from unittest.mock import patch, MagicMock, Mock


skip_below_py345 = pytest.mark.skipif((sys.version_info.major,
                                       sys.version_info.minor,
                                       sys.version_info.micro) < (3, 4, 5),
                               reason="skip test for python3.4.x")


# This is going to fail for 3.4.2 with the following error message:
# pytest.fixture functions cannot use ``yield``. Instead write and return an inner
# function/generator and let the consumer call and iterate over it.
#
@skip_below_py345
def test_repo(git_repo):
    print("Git-Repo:", git_repo)


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
