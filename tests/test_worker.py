import pytest
import os
import shutil

from unittest.mock import patch, Mock
from docstats.worker import clone_repo
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
    repo = clone_repo(SECTION, 'fake-url', PYTESTTMPDIR)
    assert repo.git_dir == GITREPO.git_dir


@patch('docstats.worker.os.path.exists')
@patch('docstats.worker.git.Repo')
def test_clone_repo(mock_repo, mock_path):
    mock_repo.clone_from = Mock(return_value=GITREPO)
    mock_path.return_value = False
    repo = clone_repo(SECTION, 'fake-url', PYTESTTMPDIR)
    assert repo.git_dir == GITREPO.git_dir