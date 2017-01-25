import pytest
import os

def test_main(capsys):
    """runs __main__.py"""
    with pytest.raises(SystemExit):
        path = os.path.dirname(os.path.realpath(__file__)) + "/../src/docstats/__main__.py"
        exec(compile(open(path).read(), path, "exec"), {}, {"__name__": "__main__"})