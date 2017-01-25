========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis|
        | |coveralls| |codecov|
        | |scrutinizer|
    * - package
      - | |version| |downloads| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |docs| image:: https://readthedocs.org/projects/docstats/badge/?style=flat
    :target: https://readthedocs.org/projects/docstats
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/openSUSE/docstats.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/openSUSE/docstats

.. |coveralls| image:: https://coveralls.io/repos/openSUSE/docstats/badge.svg?branch=master&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/r/openSUSE/docstats

.. |codecov| image:: https://codecov.io/github/openSUSE/docstats/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/openSUSE/docstats

.. |version| image:: https://img.shields.io/pypi/v/suse-docstats.svg
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/suse-docstats

.. |commits-since| image:: https://img.shields.io/github/commits-since/openSUSE/docstats/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/openSUSE/docstats/compare/v0.1.0...master

.. |downloads| image:: https://img.shields.io/pypi/dm/suse-docstats.svg
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/suse-docstats

.. |wheel| image:: https://img.shields.io/pypi/wheel/suse-docstats.svg
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/suse-docstats

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/suse-docstats.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/suse-docstats

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/suse-docstats.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/suse-docstats

.. |scrutinizer| image:: https://img.shields.io/scrutinizer/g/openSUSE/docstats/master.svg
    :alt: Scrutinizer Status
    :target: https://scrutinizer-ci.com/g/openSUSE/docstats/


.. end-badges

Statistics and Metrics for Documentation Team

* Free software: BSD license

Installation
============

::

    pip install suse-docstats

Documentation
=============

https://docstats.readthedocs.io/

Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
