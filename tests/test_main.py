import pytest
import os
from docstats.main import main


def test_main():
    """runs __main__.py"""
    with pytest.raises(SystemExit):
        path = os.path.dirname(os.path.realpath(__file__)) + "/../src/docstats/__main__.py"
        exec(compile(open(path).read(), path, "exec"), {}, {"__name__": "__main__"})


def test_main_with_empty_args():
    assert main([]) == 0