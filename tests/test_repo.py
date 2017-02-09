#

import pytest
import py
import sys


skip_below_py345 = pytest.mark.skipif((sys.version_info.major,
                                       sys.version_info.minor,
                                       sys.version_info.micro) < (3, 4, 5),
                               reason="skip test for python3.4.x")


# This is going to fail for 3.4.2 with the following error message:
# pytest.fixture functions cannot use ``yield``. Instead write and return an inner
# function/generator and let the consumer call and iterate over it.
#
@skip_below_py345
def test_repo(git_repo):
    print("Git-Repo:", git_repo)
