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
from collections import Counter, defaultdict
from git import GitCommandError

import statistics



def analyze(repo, config):
    """Analyze the repositories given at queue

    :param queue: a queue
    :type queue: :class:`queue.Queue`
    :param config: the docstats configuration contents
    :type config: :class:`configparser.ConfigParser`
    :return: dictionary with data
        data = { 'branch1': data_of_branch1,
                 'branch2': data_of_branch2,
                }
        data_of_branchX = {'doc-committers': X,
                           'additions': A,
                           'deletions': D,
                           'changes':  C,
                           'bsc': BSC,
                           'gh': GH,
                           'trello': TR,
                           ''
                           }

    :rtype: dict
    """

    target = repo.heads[0]
    wd = repo.working_tree_dir
    section = wd.rsplit("/", 1)[-1]

    for branchname, start, end in getbranches(section, config):
        try:
            repo.git.checkout(branchname)
        except GitCommandError as error:
            # error contains the following attributes:
            # ._cmd, ._cause, ._cmdline
            # .stderr, .stdout, .status, .command
            print(error)
            print(vars(error))
            print(error.status)
            print(error.command)
            print(error.stderr)
            continue

        # -----------

    print("Repo:", repo.git_dir)
    # print("Target:", target)
    # print("RootTree:", roottree)
    # print("dir", dir(repo))

    committers = Counter()
    stats = defaultdict(int)
    # additions = 0
    # deletions = 0
    # files = 0
    for idx, commit in enumerate(repo.iter_commits(repo.head), 1):
        committers[commit.author] += 1
        # datetime.fromtimestamp(commit.committed_date)
        for item in commit.stats.total:
            stats[item] += commit.stats.total[item]

        # print(idx, commit.summary)
    print("-"*10)
    print(">> Commits:", idx)
    print(">> Committers:", committers.most_common(5))
    print(">> Stats for %r:" % repo.git_dir, stats)

    return committers, stats
