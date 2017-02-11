#

from unittest.mock import patch, Mock, MagicMock
from docstats.worker import clone_repo, clone_and_analyze, tracker2int
from docstats.repo import init_tracker_dict
from docstats.utils import TRACKERS


@patch('docstats.worker.os.path.exists')
def test_clone_repo_if_path_exists(mock_path, gitrepo):
    _, repo = gitrepo
    mock_path.return_value = True
    resultrepo = clone_repo('fake-url', repo.git_dir)
    assert resultrepo.git_dir == repo.git_dir


@patch('docstats.worker.os.path.exists')
@patch('docstats.worker.git.Repo')
def test_clone_repo(mock_repo, mock_path, gitrepo):
    _, repo = gitrepo
    mock_repo.clone_from.return_value = repo
    mock_path.return_value = False

    resultrepo = clone_repo('fake-url', repo.git_dir)
    assert resultrepo.git_dir == repo.git_dir



def test_tracker2int():
    data = {}
    data['a'] = init_tracker_dict()
    tracker2int(data)
    assert data['a'] == {key: 0  for key in TRACKERS}


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

