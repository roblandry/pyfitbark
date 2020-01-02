# -*- coding: utf-8 -*-
"""PyFitBark Main Tests."""
import os

import pytest

import json

from pyfitbark.api import FitbarkApi
from pyfitbark.__main__ import argparser, MainClass, main

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


class MockResponse:
    @staticmethod
    def get_dict():
        return {"mock_key": "mock_response"}

    @staticmethod
    def get_list():
        return ["mock_response_1", "mock_response_2"]

    @staticmethod
    def get_str():
        return "mock_string"

    @staticmethod
    def get_from_file(file):
        file_data = open(os.path.join(CURRENT_DIR, "json/", f"{file}.json"), "r")
        data = json.loads(file_data.read())
        return data


class TestFitbarkMain:
    @pytest.fixture
    def api(self):
        """Return MOCK Fitbark API."""
        return MainClass()

    # FitbarkApi Replacement functions
    def get_user_profile(self, *args, **kwargs):
        return MockResponse.get_from_file("get_user_profile")

    def get_user_picture(self, *args, **kwargs):
        return MockResponse.get_from_file("get_user_picture")

    def get_user_related_dogs(self, *args, **kwargs):
        return MockResponse.get_from_file("get_user_related_dogs")

    def get_dog(self, *args, **kwargs):
        return MockResponse.get_from_file("get_dog")

    def get_dog_picture(self, *args, **kwargs):
        return MockResponse.get_from_file("get_dog_picture")

    def hass_get_token(self, *args, **kwargs):
        return MockResponse.get_str()

    def hass_get_redirect_urls(self, *args, **kwargs):
        return MockResponse.get_list()

    def hass_add_redirect_urls(self, *args, **kwargs):
        return MockResponse.get_dict()

    def hass_add_url(self, *args, **kwargs):
        return None

    def hass_remove_url(self, *args, **kwargs):
        return None

    # Tests
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

    def test_r_get(self, api, monkeypatch):
        monkeypatch.setattr(FitbarkApi, "hass_get_token", self.hass_get_token)
        monkeypatch.setattr(
            FitbarkApi, "hass_get_redirect_urls", self.hass_get_redirect_urls
        )

        data = api.r_get()
        assert isinstance(data, list)

    def test_r_reset(self, api, monkeypatch):
        monkeypatch.setattr(FitbarkApi, "hass_get_token", self.hass_get_token)
        monkeypatch.setattr(
            FitbarkApi, "hass_add_redirect_urls", self.hass_add_redirect_urls
        )

        data = api.r_reset()
        assert isinstance(data, dict)

    def test_r_add(self, api, monkeypatch):
        monkeypatch.setattr(FitbarkApi, "hass_get_token", self.hass_get_token)
        monkeypatch.setattr(FitbarkApi, "hass_add_url", self.hass_add_url)
        monkeypatch.setattr(
            FitbarkApi, "hass_get_redirect_urls", self.hass_get_redirect_urls
        )

        data = api.r_add()
        assert isinstance(data, list)

    def test_r_remove(self, api, monkeypatch):
        monkeypatch.setattr(FitbarkApi, "hass_get_token", self.hass_get_token)
        monkeypatch.setattr(FitbarkApi, "hass_remove_url", self.hass_remove_url)
        monkeypatch.setattr(
            FitbarkApi, "hass_get_redirect_urls", self.hass_get_redirect_urls
        )

        data = api.r_remove()
        assert isinstance(data, list)

    def test_u_profile(self, api, monkeypatch):
        monkeypatch.setattr(FitbarkApi, "get_user_profile", self.get_user_profile)

        data = api.u_profile()
        assert isinstance(data, dict)
        assert data["user"]["slug"] == "00000000-zzzz-1111-2222-xxxxxxxxxxxx"

    def test_u_slug(self, api, monkeypatch):
        monkeypatch.setattr(FitbarkApi, "get_user_profile", self.get_user_profile)

        data = api.u_slug()
        assert isinstance(data, str)

    def test_u_pic(self, api, monkeypatch):
        monkeypatch.setattr(FitbarkApi, "get_user_profile", self.get_user_profile)
        monkeypatch.setattr(FitbarkApi, "get_user_picture", self.get_user_picture)

        data = api.u_pic()
        assert isinstance(data, str)

    def test_u_dogs(self, api, monkeypatch):
        monkeypatch.setattr(
            FitbarkApi, "get_user_related_dogs", self.get_user_related_dogs
        )

        data = api.u_dogs()
        assert isinstance(data, dict)

    def test_u_dog_slug(self, api, monkeypatch):
        monkeypatch.setattr(
            FitbarkApi, "get_user_related_dogs", self.get_user_related_dogs
        )

        data = api.u_dog_slug()
        assert isinstance(data, list)

    def test_dog(self, api, monkeypatch):
        monkeypatch.setattr(
            FitbarkApi, "get_user_related_dogs", self.get_user_related_dogs
        )
        monkeypatch.setattr(FitbarkApi, "get_dog", self.get_dog)

        data = api.dog()
        assert isinstance(data, list)

    def test_d_pic(self, api, monkeypatch):
        monkeypatch.setattr(
            FitbarkApi, "get_user_related_dogs", self.get_user_related_dogs
        )
        monkeypatch.setattr(FitbarkApi, "get_dog_picture", self.get_dog_picture)

        data = api.d_pic()
        assert isinstance(data, list)

    def test_main(self, monkeypatch):
        monkeypatch.setattr(FitbarkApi, "hass_get_token", self.hass_get_token)
        monkeypatch.setattr(
            FitbarkApi, "hass_get_redirect_urls", self.hass_get_redirect_urls
        )
        monkeypatch.setattr(
            FitbarkApi, "hass_add_redirect_urls", self.hass_add_redirect_urls
        )
        monkeypatch.setattr(FitbarkApi, "hass_add_url", self.hass_add_url)
        monkeypatch.setattr(FitbarkApi, "hass_remove_url", self.hass_remove_url)
        monkeypatch.setattr(FitbarkApi, "get_user_profile", self.get_user_profile)
        monkeypatch.setattr(FitbarkApi, "get_user_picture", self.get_user_picture)
        monkeypatch.setattr(
            FitbarkApi, "get_user_related_dogs", self.get_user_related_dogs
        )
        monkeypatch.setattr(FitbarkApi, "get_dog", self.get_dog)
        monkeypatch.setattr(
            FitbarkApi, "get_user_related_dogs", self.get_user_related_dogs
        )
        monkeypatch.setattr(FitbarkApi, "get_dog_picture", self.get_dog_picture)

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
