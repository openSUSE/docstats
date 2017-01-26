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
from threading import current_thread
from time import sleep
import random
import git



def clone_repo(url, tmpdir):
    """Clone the Git repository

    :param str url: the URL of the Git repository
    :param str tmpdir: the temporary directory to clone to
    :return: ???
    """
    # Add here the git clone
    print("%s: Cloning url=%r to %r" % (current_thread().name, url, tmpdir))
    sleep(random.randrange(start=1, stop=6))

    # git.Repo.clone_from(url, tmpdir, progress=git.RemoteProgress())
    return "hiho"


def worker(urls, tmpdir, jobs=1):  # pragma: no cover
    """Working off all Git URLs

    :param urls: a list or generator of urls
    :param str tmpdir: the  temporary directory to clone to
    :param int jobs: integer number of workers to create [default: 1]
    """
    print("Calling worker...")
    with ThreadPoolExecutor(max_workers=jobs) as executor:
        future_to_url = {executor.submit(clone_repo, url, tmpdir): url for url in urls}
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                data = future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (url, exc))
            else:
                print('%r page is %d bytes' % (url, len(data)))
    print("Finished worker.")