========
Overview
========

.. start-badges

|travis| |codecov| |landscape| |license|


.. |travis| image:: https://travis-ci.org/openSUSE/docstats.svg?branch=develop
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/openSUSE/docstats

.. |codecov| image:: https://codecov.io/github/openSUSE/docstats/coverage.svg?branch=develop
    :alt: Coverage Status
    :target: https://codecov.io/gh/openSUSE/docstats/branch/develop

.. |landscape| image:: https://landscape.io/github/openSUSE/docstats/develop/landscape.svg?style=flat
   :target: https://landscape.io/github/openSUSE/docstats/develop
   :alt: Landscape Code Health

.. |license| image:: https://img.shields.io/badge/license-GPL3-green.svg
    :alt:
    :target: https://github.com/openSUSE/docstats/blob/master/LICENSE

.. end-badges

Statistics and Metrics for SUSE documentation team.

* Free software: GPL 3.0


Conceptual Overview
===================

The script :command:`docstats` performs the following tasks:

#. Clone the repositories that are found in the configuration file.
#. Iterate through all repositories and do:
  #. Collect the diff statistics.
  #. Collect the overall committers (usually reduced to team members only).
  #. Collect bugtracker issue numbers from commit messages.
#. Output as JSON or CSV file.


Quick Start
===========

To use the program without :command:`pip` and virtual environment (but with all
the dependencies), use the following command after cloning this repository::

    $ PYTHONPATH=src python3 -m docstats -h



Quick Start
===========

To use the program without :command:`pip` and virtual environment, use the
following command after cloning this repository::

    $ PYTHONPATH=src python3 -m docstats -h


Installation
============

To install :program:`docstats`, use the following steps:

#. Clone this repository::

    $ git clone http://github.com/openSUSE/docstats.git
    $ cd docstats

#. Create a Python 3 environment and activate it::

    $ python3 -m venv .env
    $ source .env/bin/activate

#. Optionally update the ``pip`` and ``setuptools`` modules::

    $ pip install -U pip setuptools

#. Install the package::

    $ ./setup.py develop

If you need to install it from GitHub directly, use this URL::

    git+https://github.com/openSUSE/docstats.git@develop

After the installation in your Python virtual environment, the script
:program:`docstats` is available.



Workflow
========

The script performs the following steps:

#. Clone all definied repositories into a temporary directory. The definied
   repositories are extraced from a configuration file.
#. Iterate through all cloned repositories.
#. Iterate through all commits in a single repository and extract diff statistics,
   issues, committers, and other useful information.
#. Perform statistical calculations.
#. Print all the collected information.


Contributing
============

To contribute to this project, open issues or send us pull requests. Thanks!
