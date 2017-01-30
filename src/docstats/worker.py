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

from concurrent.futures import ThreadPoolExecutor, as_completed
import multiprocessing
from threading import current_thread
from time import sleep, time
import queue
from queue import Empty
import os.path

# import pygit2
import git

from .config import geturls
# from .utils import urlparse
from .repo import analyze


def clone_repo(section, url, tmpdir):
    """Clone the Git repository

    :param str section: the section from the configuration file
    :param str url: the URL of the Git repository
    :param str tmpdir: the temporary directory to clone to
    :return: ???
    """
    # urldict = urlparse(url)
    gitdir = os.path.join(tmpdir, section)

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

class Consumer(multiprocessing.Process):
    """A consumer class which take care of the distributed work

    """
    def __init__(self, task_queue, result_queue):
        # multiprocessing.Process.__init__(self)
        super().__init__()
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        proc_name = self.name
        while True:
            next_task = self.task_queue.get()
            if next_task is None:
                # Poison pill means shutdown
                print('%s: Exiting' % proc_name)
                self.task_queue.task_done()
                break
            print('%s: %s' % (proc_name, next_task))
            answer = next_task()
            self.task_queue.task_done()
            self.result_queue.put(answer)
        return


class Producer(object):
    """A Task class to create repositories

    """
    def __init__(self, section, url, tmpdir, id):
        self.section = section
        self.url = url
        self.tmpdir = tmpdir
        self.id = id

    def __call__(self):
        repo = clone_repo(self.section, self.url, self.tmpdir)
        analyze(queue, config)
        return

    def __repr__(self):
        return "%s(%i): [%s] %r" % (type(self).__name__, self.id, self.section, self.url)

    def __str__(self):
        return '%s' % self.url


def work(config, basedir, jobs=1):
    """Working off all Git URLs

    :param config: a list or generator of urls
    :type config: :class:`configparser.ConfigParser`
    :param int jobs: integer number of workers to create [default: 1]
    :return: ???
    """
    # Establish communication queues
    tasks = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()

    urls = list(geturls(config))
    if jobs > len(urls):
        # Make sure you have not more consumers than sections in our config file
        jobs = len(urls)

    # Start consumers
    print('Creating %d consumers' % jobs)
    consumers = [Consumer(tasks, results) for _ in range(jobs)]

    start = time()
    for w in consumers:
        w.start()

    # Enqueue jobs
    num_jobs = jobs

    # for i in range(num_jobs):
    for idx, securl in enumerate(urls):
        tasks.put(Producer(*securl, tmpdir=basedir, id=idx))

    # Add a poison pill for each consumer
    for i in range(jobs):
        tasks.put(None)

    # Wait for all of the tasks to finish
    tasks.join()

    # Start printing results
    while num_jobs:
        result = results.get()
        print('Result:', result)
        num_jobs -= 1

    end = time()
    print("Finished.", end-start)