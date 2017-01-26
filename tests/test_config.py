import pytest

from docstats.config import parseconfig



@pytest.fixture# (scope="module")
def config(tmpdir):
    tmpfile = tmpdir / "docstats.ini"
    tmpfile.write("""[globals]
branch = develop

[doc-a]
url = git@github.com:SUSE/doc-a.git


[doc-b]
url = git@github.com:SUSE/doc-b.git
        """)
    return parseconfig(tmpfile.strpath)[1]



def test_parseconfig(config):
    assert config['globals']
    assert config['globals']['branch']
    sec = config.sections()
    assert config.sections() == ['doc-a', 'doc-b']
    assert config['doc-a']['url'] == 'git@github.com:SUSE/doc-a.git'