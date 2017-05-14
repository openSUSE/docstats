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

import csv
from concurrent.futures import ProcessPoolExecutor, as_completed
import logging
# from threading import current_thread
from time import time
import queue
import os.path
import git
import json

from .config import geturls
from .repo import analyze
from .utils import TRACKERS

log = logging.getLogger(__name__)


def clone_repo(url, gitdir):
    """Clone the Git repository

    :param str url: the URL of the Git repository
    :param str gitdir: the temporary directory to clone to
    :return: the repository
    :rtype: :class:`git.Repo`
    """

    if os.path.exists(gitdir):
        log.debug("URL %r alread cloned, using %r.", url, gitdir)
        return git.Repo(gitdir)

    repo = git.Repo.clone_from(url, gitdir)
    return repo


def tracker2int(data):
    """Convert the list of trackers into a number

    :param dict data: the result dictionary
    :return: None
    """
    for bug in TRACKERS:
        for key in data:
            data[key][bug] = len(data[key][bug])


def output_result(repo, result):
    """Output the results as JSON and CSV

    :param repo: the repository
    :type repo: :class:`git.Repo`
    :param dict result: the result dictionary
    :return:
    """
    wd = repo.working_tree_dir
    filename = wd + ".json"
    with open(filename, 'w') as fh:
        json.dump(result, fh, indent=4)
        log.info("Writing results to %r", filename)

    filename = wd + ".csv"
    # Make sure we have only numbers for CSV
    tracker2int(result)
    with open(filename, 'wt') as csvfile:
        # These are the fields that we are interested in
        fields = ['release',
                  'commits', 'insertions', 'deletions', 'lines',
                  'fate', 'bnc', 'bsc', 'files', 'trello', 'gh', 'doccomments',
                  'team-committers', 'external-committers',
                  ]
        writer = csv.writer(csvfile)
        writer.writerow(fields)
        for key in sorted(result):
            row = []
            row.append(key)
            row.extend([result[key][field] for field in fields[1:]])
            writer.writerow(row)
        log.info("Writing results to %r", filename)


def clone_and_analyze(url, gitdir, config):
    """Clone the GitHub repo and analyze it and save the results

    :param url: the GitHub URL to clone
    :param gitdir: the path to the temporary directory (including the section)
    :param config:
    :type config: :class:`configparser.ConfigParser`
    :return:
    """
    repo = clone_repo(url, gitdir)
    result = analyze(repo, config)
    output_result(repo, result)
    return result


def work(config, basedir, sections=None, jobs=1):
    """Working off all Git URLs

    :param config: a list or generator of urls
    :type config: :class:`configparser.ConfigParser`
    :param str basedir: the temporary base directory
    :param list sections: the sections to use
    :param int jobs: integer number of workers to create [default: 1]
    :return: ???
    """
    # Establish communication queues
    q = queue.Queue()
    urls = geturls(config, sections)

    start = time()
    with ProcessPoolExecutor(max_workers=jobs) as executor:
        future_to_url = {executor.submit(clone_and_analyze,
                                         url,
                                         os.path.join(basedir, section),
                                         config
                                         ): url for section, url in urls}
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                data = future.result()
                q.put(data)
            except (git.GitCommandError, git.CacheError, git.CommandError,
                    git.GitCommandNotFound, git.HookExecutionError, git.NoSuchPathError,
                    git.ParseError, git.RepositoryDirtyError, git.UnmergedEntriesError
                    ) as error:
                log.fatal('%r generated an exception: %s', url, error, exc_info=1)
            else:
                log.info('Got data from URL %r', url)

    end = time()
    log.info("Finished worker. Time=%.2fs", float(end - start))
    return
