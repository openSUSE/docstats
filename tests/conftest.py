import pytest

import docstats


def pytest_report_header(config):
    if config.getoption('verbose') > 0:
        return "*** Testing {} v{} ***".format(docstats.__name__, docstats.__version__)