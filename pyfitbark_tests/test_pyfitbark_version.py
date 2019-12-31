# -*- coding: utf-8 -*-
"""PyFitBark Version Tests."""
import pytest

import pyfitbark.__version__ as py_version


class TestFitbarkVersion:
    @pytest.fixture
    def api(self):
        """Return MOCK Fitbark API."""
        return py_version

    def test_version(self, api):

        # version.VERSION = (0, 0, 0)

        assert api.__version__ == "0.0.1"
