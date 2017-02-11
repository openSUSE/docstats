#

import pytest
import docstats.cli
from docstats.cli import parsecli, checkcliargs

from docopt import DocoptExit


@pytest.mark.parametrize('cli,expected', [
    # 1 - just the config file
    (['foo.ini'],
     {'CONFIGFILE': 'foo.ini'}
     ),
    # 2 - with one verbose
    (['-v', 'foo.ini'],
     {'CONFIGFILE': 'foo.ini', '-v': 1}
     ),
    # 3 - with double verbose
    (['-vv', 'foo.ini'],
     {'CONFIGFILE': 'foo.ini', '-v': 2}
     ),
    # 4 - with triple verbose
    (['-vvv', 'foo.ini'],
     {'CONFIGFILE': 'foo.ini', '-v': 3}
     ),
    # 5 -- jobs
    (['-j 1', 'foo.ini'],
     {'CONFIGFILE': 'foo.ini', '--jobs': 1}
     ),
    # 6 -- jobs
    (['--jobs=2', 'foo.ini'],
     {'CONFIGFILE': 'foo.ini', '--jobs': 2}
     ),
    # 7 - fail --jobs
    pytest.mark.xfail((['--jobs=x', 'foo.ini'], {} )),
    # 8
    (['-s', 'bar', 'foo.ini'],
     {'CONFIGFILE': 'foo.ini', '--sections': ['bar']}),
    # 9
    (['--sections', 'bar', 'foo.ini'],
     {'CONFIGFILE': 'foo.ini', '--sections': ['bar']}),
    # 10
    (['--sections=bar', 'foo.ini'],
     {'CONFIGFILE': 'foo.ini', '--sections': ['bar']}),
    # 11
    (['--sections', 'bar,baz', 'foo.ini'],
     {'CONFIGFILE': 'foo.ini', '--sections': ['bar', 'baz']}),
    # 12
    (['--sections=bar,baz', 'foo.ini'],
     {'CONFIGFILE': 'foo.ini', '--sections': ['bar', 'baz']}),

])
def test_parsecli(cli, expected, monkeypatch):

    monkeypatch.setattr(docstats.cli.os.path, 'exists', lambda x: True)

    result = parsecli(cli)
    # Create set difference and only compare this with the expected dictionary
    assert {item: result.get(item, None) for item in expected} == expected



def test_checkcliargs_with_FileNotFoundError():
    with pytest.raises(FileNotFoundError):
        checkcliargs({'--jobs': '1', 'CONFIGFILE': 'fake', '--sections': None})


def test_checkcliargs_with_DocoptExit():
    with pytest.raises(DocoptExit):
        checkcliargs({'--jobs': 'x', 'CONFIGFILE': None})
