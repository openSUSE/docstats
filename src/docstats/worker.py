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

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from threading import current_thread
from time import time
import queue
import os.path


import git

from .config import geturls
from .repo import analyze


def clone_repo(url, gitdir):
    """Clone the Git repository

    :param str section: the section from the configuration file
    :param str url: the URL of the Git repository
    :param str tmpdir: the temporary directory to clone to
    :return: ???
    """

    if os.path.exists(gitdir):
        print("URL {!r} alread cloned, using {!r}.".format(url, gitdir))
        # return pygit2.Repository(gitdir)
        return git.Repo(gitdir)

    print("%s: Cloning url=%r to %r" % (current_thread().name, url, gitdir))
    start = time()
    repo = git.Repo.clone_from(url, gitdir)
    # repo = pygit2.clone_repository(url, gitdir )  # pygit2.UserPass('', '')
    end = time()
    return repo


def cloner(config, basedir, jobs=1):  # pragma: no cover
    """Working off all Git URLs

    :param config: a list or generator of urls
    :type config: :class:`configparser.ConfigParser`
    :param int jobs: integer number of workers to create [default: 1]
    """
    # See also: http://www.codekoala.com/posts/command-line-progress-bar-python/
    print("Calling worker...")
    q = queue.Queue()

    urls = geturls(config)

    start = time()
    with ThreadPoolExecutor(max_workers=jobs) as executor:
        future_to_url = {executor.submit(clone_repo, section, url, basedir): url for section, url in urls}
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                data = future.result()
                q.put(data)
            # TODO: Make exceptions more explicit
            except Exception as exc:
                print('%r generated an exception: %s' % (url, exc))
            else:
                print('Got from URL %r: %s' % (url, data))

    end = time()
    print("Finished worker. Time={:.1f}".format(float(end - start)))
    print("Queue:", q)
    return q

# ---------------------------------------------------------------------

def clone_and_analyze(url, gitdir, config):
    """Clone the GitHub repo and analyze it

    :param url: the GitHub URL to clone
    :param gitdir: the path to the temporary directory (including the section)
    :param config:
    :type config: :class:`configparser.ConfigParser`
    :return:
    """
    repo = clone_repo(url, gitdir)
    return analyze(repo, config)



def work(config, basedir, jobs=1):
    """Working off all Git URLs

    :param config: a list or generator of urls
    :type config: :class:`configparser.ConfigParser`
    :param int jobs: integer number of workers to create [default: 1]
    :return: ???
    """
    # Establish communication queues
    q = queue.Queue()
    urls = geturls(config)

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
            # TODO: Make exceptions more explicit
            except Exception as exc:
                print('%r generated an exception: %s' % (url, exc))
            else:
                print('Got from URL %r: %s' % (url, data))

    end = time()
    print("Finished worker. Time={:.1f}".format(float(end - start)))
    return
