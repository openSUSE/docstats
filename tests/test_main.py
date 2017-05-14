#

from docopt import DocoptExit
import pytest
import os

from docstats.cli import main
from unittest.mock import patch, Mock
from configparser import ConfigParser, DuplicateSectionError, DuplicateOptionError


def test_main(capsys):
    """Checks, if __main__.py can be executed"""
    with pytest.raises(SystemExit):
        path = os.path.dirname(os.path.realpath(__file__)) + \
            "/../src/docstats/__main__.py"
        exec(compile(open(path).read(), path, "exec"),
             {}, {"__name__": "__main__"})


def test_main_with_empty_args():
    with pytest.raises(DocoptExit):
        main([])


@pytest.mark.parametrize('error', [
    KeyboardInterrupt,
    FileNotFoundError, OSError,
    DuplicateSectionError('fake-sec'),
    DuplicateOptionError('fake-sec', 'fake-opt'),
])
@patch('docstats.cli.parsecli')
def test_main_with_ctrl_c(mock_parsecli, error):
    mock_parsecli.side_effect = error
    result = main([])
    assert result


@patch('docstats.worker.work')
@patch('docstats.cli.os.makedirs')
@patch('docstats.cli.gettmpdir')
@patch('docstats.cli.parseconfig')
@patch('docstats.cli.parsecli')
def test_main_return_with_0(mock_parsecli, mock_parseconfig, mock_gettmpdir,
                            mock_makedirs, mock_work):
    def work(config, basedir, sections, jobs):
        return True

    def gettmpdir(path):
        return True

    mock_parsecli.return_value = {'--jobs': 1,
                                  '--sections': [],
                                  '-v': 2,
                                  'CONFIGFILE': 'fake.ini',
                                  }
    mock_config = Mock(autospec=ConfigParser)
    mock_config.get.return_value = 'section'
    mock_config.sections.return_value = []

    mock_parseconfig.return_value = ('fake.ini', mock_config)
    mock_gettmpdir.side_effects = gettmpdir
    mock_makedirs.return_value = True
    mock_work.side_effects = work

    assert not main()
