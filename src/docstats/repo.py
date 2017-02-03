#
# Copyright (c) 2017 SUSE Linux GmbH
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA
#

from .config import getbranches
from .log import log
from git import GitCommandError
import json
from .utils import findbugid, TRACKERS

import statistics


def collect_diffstats(commit, dictresult):
    """Collect all the diff statistics like additions, deletions, file changes etc.

    :param commit: the commit
    :type commit: :class:`git.Commit`
    :param dict dictresult: the result of the dictionary
    """
    for item in commit.stats.total:
            dictresult[item] += commit.stats.total[item]


def collect_committers(commit, dictresult):
    """Collect all the committers

    :param commit:  the commit
    :type commit: :class:`git.Commit`
    :param dict dictresult: the result of the dictionary
    """
    pass



def collect_issues(commit, dictresult):
    """Collect all the issues that can be find in a commit message

    :param commit:  the commit
    :type commit: :class:`git.Commit`
    :param dict dictresult: the result of the dictionary; the dict will be changed after the
                            function has been called
    """

    # Initialize the trackers with an empty set if needed
    for tracker in TRACKERS:
        if not dictresult.get(tracker):
            dictresult[tracker] = []

    # Go through each summary and message and try to find issue tracker information
    for msg in [commit.summary, commit.message]:
        for tracker, issue in findbugid(msg):
            if tracker in TRACKERS:
                dictresult[tracker].append(issue)
            elif tracker[:3] in ('fix', 'clo', 'res'):
                dictresult['gh'].append(issue)

    return dictresult


def iter_commits(repo, dictresult, branchname, start=None, end=None):
    """Iterate through all commits

    :param repo: a repository
    :type repo: :class:`git.Repo`
    :param dict dictresult: the result of the dictionary; the dict will be changed after the
                            function has been called
    :param str branchname: the name of the branch
    :param start: the start position or None
    :param end: the end position or None
    :return:
    """
    start = '' if start is None else start
    end = '' if end is None else end

    rev = "..".join([start, end])
    if rev == '..':
        rev = repo.head

    log.info("Using start=%r, end=%r -> rev=%r", start, end, rev)

    for idx, commit in enumerate(repo.iter_commits(rev), 1):
        # Collect the statistics information
        collect_diffstats(commit, dictresult[branchname])

        # Collect the committers
        collect_committers(commit, dictresult[branchname])

        # Collect the bug issues from different trackers
        collect_issues(commit, dictresult[branchname])

    # Save overall commits:
    dictresult[branchname]['commits'] = idx

    return dictresult


def init_stats_dict():
    """Create a dictionary statistics object with defaults to zero for;
       used for counting

    :return: dictionary with all values to zero
    :rtype: dict
    """
    return {item: 0 for item in ('deletions', 'files', 'insertions', 'lines')}


def cleanup_dict(dictresult):
    """Cleanup step to turn all sets into list to make sure it is serialized by JSON

    :param dict dictresult: the result of the dictionary; the dict will be changed after the
                            function has been called
    """
    for branch in dictresult:
        for tracker in TRACKERS:
            dictresult[branch][tracker] = list(set(dictresult[branch][tracker]))



def analyze(repo, config):
    """Analyze the repositories given at queue

    :param repo: a repository
    :type repo: :class:`git.Repo`
    :param config: the docstats configuration contents
    :type config: :class:`configparser.ConfigParser`
    :return: dictionary with data
        data = { 'branch1': data_of_branch1,
                 'branch2': data_of_branch2,
                }
        data_of_branchX = {'doc-committers': X, # type:set
                           'additions': A,      # type:int
                           'deletions': D,      # type:int
                           '#commits': N,       # type:int
                           'changes':  C,       # type:int
                           'bsc': BSC,          # type:set
                           'gh': GH,            # type:set
                           'fate': FA,          # type:set
                           'trello': TR,        # type:set
                           'doccomments: DC',   # type:set
                           'start-commit': SC   # type:str
                           'end-commit': EC     # type:str
                           }
    :rtype: dict
    """

    result = {}
    wd = repo.working_tree_dir
    section = wd.rsplit("/", 1)[-1]

    # Check if we have a "branches" section in the config. If not, fallback
    # to develop branch:
    urls = list(getbranches(config.get(section, 'branches', fallback=None)))
    if not urls:
       branchname = config.get(section, 'branch', fallback=None)
       start =  config.get(section, 'start', fallback='')
       end =  config.get(section, 'end', fallback='')

       if not branchname:
          # Use our default branch...
          branchname = 'develop'
       urls = [(branchname, start, end)]


    for branchname, start, end in urls:
        result[branchname] = {}
        result[branchname]['start'] = str(start)
        result[branchname]['end'] = str(end)
        try:
            # head = repo.create_head(branchname)
            # head.checkout(branchname)
            repo.git.checkout(branchname)
        except GitCommandError as error:
            # error contains the following attributes:
            # ._cmd, ._cause, ._cmdline
            # .stderr, .stdout, .status, .command
            log.error(error)
            # We want to have it in the result dict too:
            result[branchname] = {'error': error}
            continue

        log.info("Investigating repo %r on branch %r...", repo.git_dir, branchname)

        result[branchname].update(init_stats_dict())
        iter_commits(repo, result, branchname, start, end)

    cleanup_dict(result)

    log.debug("Result dict is %r", result)

    jsonfile = wd + ".json"
    with open(jsonfile, 'w') as fh:
        json.dump(result, fh, indent=4)
        log.debug("Writing results to %r", jsonfile)

    return result
