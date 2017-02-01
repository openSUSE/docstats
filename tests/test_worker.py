import pytest
import os
import shutil

from unittest.mock import patch, Mock, MagicMock
from docstats.worker import clone_repo, clone_and_analyze
import git

USER = os.environ["USER"]
PYTESTTMPDIR = "/tmp/pytest-of-%s/" % USER
SECTION = "git-test-repo"
GITDIR =  os.path.join(PYTESTTMPDIR, SECTION)
GITREPO = None


@pytest.fixture(scope="module",)
def gitrepo():
    global GITREPO, GITDIR
    if GITREPO is None:
        GITREPO = git.Repo.init(GITDIR, mkdir=True)
    yield GITREPO
    GITREPO = None
    shutil.rmtree(GITDIR)



def test_clone_repo_if_path_exists(gitrepo):
    repo = clone_repo('fake-url', os.path.join(PYTESTTMPDIR, SECTION))
    assert repo.git_dir == GITREPO.git_dir


@patch('docstats.worker.os.path.exists')
@patch('docstats.worker.git.Repo')
def test_clone_repo(mock_repo, mock_path):
    mock_repo.clone_from = Mock(return_value=GITREPO)
    mock_path.return_value = False
    repo = clone_repo('fake-url', os.path.join(PYTESTTMPDIR, SECTION))
    assert repo.git_dir == GITREPO.git_dir


#@patch('docstats.repo.analyze')
#@patch('docstats.worker.clone_repo')
#def test_clone_and_analyze(mock_clone, mock_analyze):
#    # clone_and_analyze(url, gitdir, config)
#    mock_clone.return_value = MagicMock()# 'fake-url'
#    mock_clone.mock_add_spec(git.Repo)
#    mock_clone.heads.__getitem__.return_value = 'develop'
#    mock_clone.head.return_value = 'develop'
#    mock_clone.iter_commits.return_value = ['a', 'b']
#
#    mock_analyze.return_value = "repo_result"
#    config = Mock()
#
#    # with patch.object()
#    result = clone_and_analyze("fake-url", os.path.join(PYTESTTMPDIR, SECTION), config)
#    assert mock_clone.called
#    assert mock_analyze.called

