# -*- coding: utf-8 -*-
"""PyFitBark Version Tests."""
import pytest

import pyfitbark.__main__ as py_main


class TestFitbarkVersion:
    @pytest.fixture
    def api(self):
        """Return MOCK Fitbark API."""
        return py_main

    def test_main(self, api):
        api = self.api
