#

import pytest
import py

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


def test_geturls():
    urls = list(geturls(config))
    assert len(urls) == 2
    assert urls == [('doc-a', 'git://doc-a.git'), ('doc-b', 'git://doc-b.git')]


@pytest.mark.parametrize('string,expected', [
    #
    (None, []),
    #
    ('', []),
    #
    ('''br/a
    ''', [('br/a', '', '')]),
    #
    ('''
 # br/null  adfadf..affee
 br/a   abc..def
 # This is an additional comment
 br/b
''', [('br/a', 'abc', 'def'), ('br/b', '', '')]),
    #
    ('''
 # br/null  adfadf..affee
 br/a   abc..
 br/b   ..def
 br/c   bcd..eff
''', [('br/a', 'abc', ''), ('br/b', '', 'def'), ('br/c', 'bcd', 'eff')])

])
def test_getbranches(string, expected):
    assert list(getbranches(string)) == expected

    #branches = list(getbranches('doc-b', config))
    #expected = [('maint/a',  '',     ''),
    #            ('maint/b',  'abce', ''),
    #            ('maint/c',  '',     'f123'),
    #            ('maint/d',  'abce', ''),
    #            ('maint/e',  '1234', '345a')
    #            ]
    #assert branches
    #assert len(branches) == 5
    #assert branches == expected


@pytest.mark.parametrize('string,expected', [
    #
    ('maintenance/SLE12',            [('maintenance/SLE12', '', '')]),
    #
    (' maintenance/SLE12   abc\n',   [('maintenance/SLE12', 'abc', '')]),
    #
    ('maintenance/SLE12   abc..',    [('maintenance/SLE12', 'abc', '')]),
    #
    ('maintenance/SLE12   ..abc',    [('maintenance/SLE12', '', 'abc')]),
    #
    ('maintenance/SLE12   abc..def', [('maintenance/SLE12', 'abc', 'def')]),
])
def test_getbranchparts(string, expected):
    assert list(getbranchparts(string)) == expected
