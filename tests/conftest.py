import pytest

import docstats
import git
from contextlib import contextmanager
import os
from py.path import local


def pytest_report_header(config):
    if config.getoption('verbose') > 0:
        return "*** Testing {} v{} ***".format(docstats.__name__, docstats.__version__)


# -------------------------------------------------------------------
# taken from _pytest.tmpdir
def get_user():
    """Return the current user name, or None if getuser() does not work
    in the current environment (see #1010).

    :return: current user name
    :rtype: str
    """
    import getpass
    try:
        return getpass.getuser()
    except (ImportError, KeyError):
        return None


# taken from _pytest.tmpdir
def get_pytest_roottmpdir():
    """Returns the temporary root directory of pytest (usually something like
       "/tmp/pytest-of-$USER/"

    :return: root temporary directory of pytest
    :rtype: :class:`py.path.local`
    """
    temproot = local.get_temproot()
    user = get_user()
    rootdir = temproot.join('pytest-of-%s' % user) if user else temproot
    rootdir.ensure(dir=True)
    return rootdir


# -------------------------------------------------------------------
@contextmanager
def changedir(path):
    """Contextmanager: Switch to given path and restore old path afterwards

    :param path: path
    :type path: str | :class:`py.path.local`
    :return: old directory path
    """
    cwd = local(path).chdir()
    yield cwd
    cwd.chdir()


def gittmpdir():
    """Return a "numbered" temporary Git repository

    :return: the path to the temporary Git repository, usually something like
             local('/tmp/pytest-of-toms/gitrepo-X') whereas X is an integer
     :rtype: :class:`py.path.local`
    """
    rootdir = get_pytest_roottmpdir()
    return local.make_numbered_dir(prefix='gitrepo-', rootdir=rootdir)


@pytest.fixture(scope="session")
def git_repo():
    """Fixture to create a test Git repository with several commits

    :return: temporary repository
    :rtype: :class:`git.Repo`
    """
    gtmpdir = gittmpdir()
    result = {}
    repo = git.Repo.init(path=gtmpdir.strpath, mkdir=True)

    tux = git.Actor('Tux Penguin', 'tux@example.org')
    wilber = git.Actor("Wilber Gimp", 'wilber@example.net')
    committers = [tux, wilber]
    with changedir(gtmpdir) as cwd:
        # Create two files
        local("fox.txt").write("The quick brown fox")
        local("README.txt").write("This is a test repository")

        repo.index.add(['fox.txt', 'README.txt'])
        repo.index.commit("First commit", committer=tux, author=tux)

        local("fox.txt").write("jumps over the lazy dog.", mode="a")
        repo.index.add(['fox.txt'])
        repo.index.commit("Add another line", committer=tux, author=tux)

        local("README.txt").write("==================", mode="a")
        repo.index.add(['README.txt'])
        repo.index.commit("Add equal sign line", committer=wilber, author=wilber)


    # Create some statistics
    result['commits'] = 3
    result['committer_mails'] = {user.email for user in committers}
    yield result, repo

    # Possible removal of the git repo
