import pytest

from docstats.cli import parsecli


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
])
def test_parsecli(cli, expected):
    result = parsecli(cli)
    # Create set difference and only compare this with the expected dictionary
    assert {item: result.get(item, None) for item in expected} == expected