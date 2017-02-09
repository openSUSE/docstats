.. docstats documentation master file for manpage

:orphan:

docstats -- Manual Page
===========================


Synopsis
--------
::

 docstats [OPTIONS] CONFIGFILE


Description
-----------

The programm :command:`docstats` analyzes local Git repositories and outputs
collected data like:

* number of committers belonging to a team
* number of external contributors
* number of overall committs
* name of different branches
* number of Bugzilla, GitHub, Fate, and Trello issues
* etc.


Conceptual Overview
-------------------

The script :command:`docstats` performs the following tasks:

#. Clone the repositories that are found in the configuration file.
#. Iterate through all repositories and collect all neccessary information.
#. Output as JSON file.


Options
-------

.. program:: docstats

.. option:: -h, --help

   Display usage summary

.. option:: --version

   Prints the version

.. option:: -v...

   Raise verbosity level; can be used more than once

.. option:: CONFIGFILE

   The configuration file which contains all to repositories to investigate

.. option:: --sections <SECTIONS>, -s <SECTIONS>

   Select one or more sections from configuration file only (default all)


Examples
--------

* Clone and investigate everything in the configuration file::

   docstats myconfig.ini

* Clone and investigate only the section named `doc-sle`::

   docstats --sections=doc-sle myconfig.ini

* Clone and investigate everything in the configuration file but distribute
  the work to four CPUs::

   docstats -j4 myconfig.ini


Diagnostics
-----------

:program:`docstats` return zero when successful and not equal to zero when
some errors happend.


Author
------

   Thomas Schraitle <toms(AT)opensuse.org>
