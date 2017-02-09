#

from docopt import DocoptExit
import pytest
import os
import sys

from docstats.main import main



@pytest.mark.skip
def test_main():
    """runs __main__.py"""
    with pytest.raises(SystemExit):
        path = os.path.dirname(os.path.realpath(__file__)) + "/../src/docstats/__main__.py"
        exec(compile(open(path).read(), path, "exec"), {}, {"__name__": "__main__"})


def test_main_with_empty_args():
    with pytest.raises(DocoptExit):
        main([])