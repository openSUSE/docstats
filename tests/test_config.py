#

import pytest
import py
from unittest.mock import patch

from docstats.config import parseconfig, geturls, getbranches, getbranchparts

# Our global variables which is used in our configuration parser
# will be overwritten bei setup_module()
config = None
configfiles = None
tmpdir = None
tmpfile = None


def setup_module(module):
    if config is not None:
        return

    try:
        module.tmpdir = py.path.local('/tmp').mkdtemp()

    except py.error.EEXIST:
        module.tmpdir = py.path.local('/tmp/pytest/config')
    module.tmpfile = tmpdir / "docstats.ini"
    module.tmpfile.write("""[globals]
branch = develop

[doc-a]
url = git://doc-a.git

[doc-b]
url = git://doc-b.git
branches =
    maint/a
    maint/b  abce
    maint/c  ..f123
    maint/d  abce..
    maint/e  1234..345a
    # maint/f  1234..56789

[doc-c]
url =
        """)
    # module is our global scope
    module.configfiles, module.config = parseconfig(tmpfile.strpath)


def teardown_module(module):
    module.tmpdir.remove(ignore_errors=True)


# --------------------------------------------------------
def test_config_files():
    assert len(configfiles) == 1

def test_config_global():
    assert config['globals']

def test_config_global_branch():
    assert config['globals']['branch']

def test_config_sections():
    sec = config.sections()
    assert config.sections() == ['doc-a', 'doc-b', 'doc-c']

def test_config_url():
    assert config['doc-a']['url'] == 'git://doc-a.git'


# --------------------------------------------------------
def test_geturls():
    urls = list(geturls(config))
    assert len(urls) == 2
    assert urls == [('doc-a', 'git://doc-a.git'), ('doc-b', 'git://doc-b.git')]


def test_geturls_with_section():
    urls = list(geturls(config, ['doc-a']))
    assert len(urls) == 1
    assert urls == [('doc-a', 'git://doc-a.git'),]


def test_geturls_with_section_and_empty_url():
    urls = list(geturls(config, ['doc-c']))
    assert urls == []


def test_geturls_with_unknown_section():
    urls = list(geturls(config, ['missing']))
    assert urls == []


@patch('docstats.config.ConfigParser')
def test_geturls_with_patching(mock_config):
    mock_config.sections.return_value = ['foo']
    mock_config.get.return_value = 'url-value'
    urls = list(geturls(mock_config))
    assert urls == [('foo', 'url-value')]


# --------------------------------------------------------
@pytest.mark.parametrize('string,expected', [
    #
    (None, []),
    #
    ('', []),
    #
    ('''name br/a
    ''', [('name', 'br/a', '', '')]),
    #
    ('''
 # br/null  adfadf..affee
 name br/a   abc..def
 # This is an additional comment
 name br/b
''', [('name', 'br/a', 'abc', 'def'), ('name', 'br/b', '', '')]),
    #
    ('''
 # br/null  adfadf..affee
 name  br/a   abc..
 name br/b   ..def
 name br/c   bcd..eff
''', [('name', 'br/a', 'abc', ''),
      ('name', 'br/b', '', 'def'),
      ('name', 'br/c', 'bcd', 'eff')])

])
def test_getbranches(string, expected):
    assert list(getbranches(string)) == expected


@pytest.mark.parametrize('string,expected', [
    #
    ('name',                              [('name', 'develop', '', '')]),
    #
    ('name maintenance/SLE12',            [('name', 'maintenance/SLE12', '', '')]),
    #
    (' name maintenance/SLE12   abc\n',   [('name', 'maintenance/SLE12', 'abc', '')]),
    #
    ('name maintenance/SLE12   abc..',    [('name', 'maintenance/SLE12', 'abc', '')]),
    #
    ('name maintenance/SLE12   ..abc',    [('name', 'maintenance/SLE12', '', 'abc')]),
    #
    ('name maintenance/SLE12   abc..def', [('name', 'maintenance/SLE12', 'abc', 'def')]),
])
def test_getbranchparts(string, expected):
    assert list(getbranchparts(string)) == expected
