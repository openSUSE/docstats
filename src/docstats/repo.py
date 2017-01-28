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

#prev = None
#for idx, cur in enumerate(repo.walk(repo.head.target)):
#
#    if prev is not None:
#        print(prev.id)
#        diff = cur.tree.diff_to_tree(prev.tree)
#        for patch in diff:
#            print(patch.status, ':', patch.new_file_path, end='')
#            if patch.new_file_path != patch.old_file_path:
#                print('(was %s)' % patch.old_file_path, end='')
#            print()
#
#    if cur.parents:
#        prev = cur
#        cur = cur.parents[0]
#print(">>> Number of iterations: %s" % idx)

from collections import Counter, defaultdict


def analyze(queue, config):
    """Analyze the repositories given at queue

    :param queue: a queue
    :type queue: :class:`queue.Queue`
    :param config: the docstats configuration contents
    :type config: :class:`configparser.ConfigParser`
    :return:
    """
    while not queue.empty():
        repo = queue.get()
        if repo.working_dir.count("sleha"):
            break

    target = repo.heads[0]
    roottree = repo.tree(target)

    print("Repo:", repo)
    print("Target:", target)
    print("RootTree:", roottree)
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
    print(">> Stats:", stats)
