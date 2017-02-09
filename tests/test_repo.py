#

import pytest
import py
import sys


skip_below_py345 = pytest.mark.skipif((sys.version_info.major,
                                       sys.version_info.minor,
                                       sys.version_info.micro) < (3, 4, 5),
                               reason="skip test for python3.4.x")


@skip_below_py345
def test_repo(git_repo):
    print("Git-Repo:", git_repo)
