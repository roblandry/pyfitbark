# -*- coding: utf-8 -*-
"""PyFitBark Main Tests."""
import os

import httpretty

import pytest

from argparse import ArgumentParser

from pyfitbark.__main__ import argparser, MainClass, main


class TestFitbarkMain:
    @pytest.fixture
    def api(self):
        """Return MOCK Fitbark API."""
        return MainClass()

    # def test_main(self, api):
    #     api = self.api

    def test_argparser(self):
        opts = argparser([])
        assert not opts.user

        opts = argparser(["-g"])
        assert opts.get

        opts = argparser(["-r"])
        assert opts.reset

        opts = argparser(["-a"])
        assert opts.add

        opts = argparser(["-x"])
        assert opts.remove

        opts = argparser(["-u"])
        assert opts.user

        opts = argparser(["--user-slug"])
        assert opts.user_slug

        opts = argparser(["--user-pic"])
        assert opts.user_pic

        opts = argparser(["-d"])
        assert opts.dogs

        opts = argparser(["--dog-slug"])
        assert opts.dog_slug

        opts = argparser(["--dog"])
        assert opts.dog

        opts = argparser(["--dog-pic"])
        assert opts.dog_pic

    def test_r_get(self, api):
        data = api.r_get()
        assert isinstance(data, list)

    def test_r_reset(self, api):
        data = api.r_reset()
        assert isinstance(data, dict)

    def test_r_add(self, api):
        data = api.r_add()
        assert isinstance(data, list)

    def test_r_remove(self, api):
        data = api.r_remove()
        assert isinstance(data, list)

    def test_u_profile(self, api):
        data = api.u_profile()
        assert isinstance(data, dict)

    def test_u_slug(self, api):
        data = api.u_slug()
        assert isinstance(data, str)

    def test_u_pic(self, api):
        data = api.u_pic()
        assert isinstance(data, str)

    def test_u_dogs(self, api):
        data = api.u_dogs()
        assert isinstance(data, dict)

    def test_u_dog_slug(self, api):
        data = api.u_dog_slug()
        assert isinstance(data, list)

    def test_dog(self, api):
        data = api.dog()
        assert isinstance(data, list)

    def test_d_pic(self, api):
        data = api.d_pic()
        assert isinstance(data, list)

    def test_main(self):
        main([])
        # main(['-h'])
        main(["-g"])
        main(["-r"])
        main(["-a"])
        main(["-x"])
        main(["-u"])
        main(["--user-slug"])
        main(["--user-pic"])
        main(["-d"])
        main(["--dog-slug"])
        main(["--dog"])
        main(["--dog-pic"])
