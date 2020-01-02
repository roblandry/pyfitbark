# -*- coding: utf-8 -*-
"""PyFitBark Main Tests."""
import os
import builtins
import io
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
    def get_tuple():
        return ("mock_response_1", "mock_response_2")

    @staticmethod
    def get_list():
        return ["mock_response_1", "mock_response_2"]

    @staticmethod
    def get_str():
        return "mock_string"

    @staticmethod
    def get_from_file(file):
        # file_data = open(os.path.join(CURRENT_DIR, "json/", f"{file}.json"), "r")

        if "get_user_profile" in file:
            data = io.StringIO(
                '{"user": { "slug": "00000000-zzzz-1111-2222-xxxxxxxxxxxx" } }'
            )
        elif "get_user_picture" in file:
            data = io.StringIO(
                '{"image": {"data": "/9j/4AAQSkZJRgABAQAASABIAAD/4QBYRXhpZgAATU0AKgAAAA" } }'
            )
        elif "get_user_related_dogs" in file:
            data = io.StringIO(
                '{"dog_relations": [{ "dog": { "slug": "036aa64a-96cc-4fec-bee9-2e3c843208a0" } } ] }'
            )
        elif "get_dog_picture" in file:
            data = io.StringIO(
                '{"image": {"data": "/9j/4AAQSkZJRgABAQAASABIAAD/4QBYRXhpZgAATU0AKgAAAA" } }'
            )
        elif "get_dog" in file:
            data = io.StringIO(
                '{"dog": { "slug": "036aa64a-96cc-4fec-bee9-2e3c843208a0", "name": "Rose" } }'
            )

        # data = json.loads(file_data.read())
        data = json.loads(data.read())
        return data

    @staticmethod
    def token_file_new():
        data = io.StringIO(
            '{"client_id": "INSERT IT HERE", "client_secret": "INSERT IT HERE"}'
        )
        return data

    @staticmethod
    def token_file_good():
        data = io.StringIO(
            '{"client_id": "Mock Client ID", "client_secret": "Mock Client Secret"}'
        )
        return data


class TestFitbarkMain:
    @pytest.fixture
    def api(self, monkeypatch):
        """Return MOCK Fitbark API."""
        monkeypatch.setattr(builtins, "open", self.token_file_good)
        monkeypatch.setattr(os.path, "isfile", self.os_path_isfile_true)
        monkeypatch.setattr(
            FitbarkApi, "get_authorization_url", self.get_authorization_url
        )
        monkeypatch.setattr(builtins, "input", self.input)
        monkeypatch.setattr(FitbarkApi, "request_token", self.request_token)

        return MainClass()

    # Other Replacement functions
    def os_path_isfile_true(self, *args, **kwargs):  # pylint: disable=unused-argument
        return True

    def os_path_isfile_false(self, *args, **kwargs):  # pylint: disable=unused-argument
        return False

    def io_error(self, *args, **kwargs):  # pylint: disable=unused-argument
        raise IOError

    def token_file_good(self, *args, **kwargs):  # pylint: disable=unused-argument
        return MockResponse.token_file_good()

    def token_file_new(self, *args, **kwargs):  # pylint: disable=unused-argument
        return MockResponse.token_file_new()

    def input(self, *args, **kwargs):  # pylint: disable=unused-argument
        return MockResponse.get_str()

    def handle_secrets(self, *args, **kwargs):  # pylint: disable=unused-argument
        return json.loads(MockResponse.token_file_new().read())

    # Main Replacement functions
    def set_token(self, *args, **kwargs):  # pylint: disable=unused-argument
        return True

    # FitbarkApi Replacement functions
    def get_authorization_url(self, *args, **kwargs):  # pylint: disable=unused-argument
        return MockResponse.get_tuple()

    def request_token(self, *args, **kwargs):  # pylint: disable=unused-argument
        return MockResponse.get_dict()

    def get_user_profile(self, *args, **kwargs):  # pylint: disable=unused-argument
        return MockResponse.get_from_file("get_user_profile")

    def get_user_picture(self, *args, **kwargs):  # pylint: disable=unused-argument
        return MockResponse.get_from_file("get_user_picture")

    def get_user_related_dogs(self, *args, **kwargs):  # pylint: disable=unused-argument
        return MockResponse.get_from_file("get_user_related_dogs")

    def get_dog(self, *args, **kwargs):  # pylint: disable=unused-argument
        return MockResponse.get_from_file("get_dog")

    def get_dog_picture(self, *args, **kwargs):  # pylint: disable=unused-argument
        return MockResponse.get_from_file("get_dog_picture")

    def hass_get_token(self, *args, **kwargs):  # pylint: disable=unused-argument
        return MockResponse.get_str()

    def hass_get_redirect_urls(
        self, *args, **kwargs
    ):  # pylint: disable=unused-argument
        return MockResponse.get_list()

    def hass_add_redirect_urls(
        self, *args, **kwargs
    ):  # pylint: disable=unused-argument
        return MockResponse.get_dict()

    def hass_add_url(self, *args, **kwargs):  # pylint: disable=unused-argument
        return None

    def hass_remove_url(self, *args, **kwargs):  # pylint: disable=unused-argument
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

    def test_load_file(self, api, monkeypatch):
        monkeypatch.setattr(api, "handle_secrets", self.handle_secrets)

        with pytest.raises(SystemExit):
            api.load_file()

    def test_handle_secrets(self, api, monkeypatch):
        monkeypatch.setattr(builtins, "open", self.io_error)
        with pytest.raises(SystemExit):
            with pytest.raises(IOError):
                api.handle_secrets()

        monkeypatch.setattr(builtins, "open", self.token_file_good)

        monkeypatch.setattr(os.path, "isfile", self.os_path_isfile_false)
        with pytest.raises(SystemExit):
            api.handle_secrets()

        monkeypatch.setattr(os.path, "isfile", self.os_path_isfile_true)
        data = api.handle_secrets()
        assert isinstance(data, dict)

    def test_do_auth(self, api, monkeypatch):
        monkeypatch.setattr(os.path, "isfile", self.os_path_isfile_false)
        monkeypatch.setattr(
            FitbarkApi, "get_authorization_url", self.get_authorization_url
        )
        monkeypatch.setattr(builtins, "input", self.input)
        monkeypatch.setattr(FitbarkApi, "request_token", self.request_token)
        monkeypatch.setattr(api, "set_token", self.set_token)

        api.do_auth()

    def test_get_token(self, api, monkeypatch):
        monkeypatch.setattr(builtins, "open", self.io_error)
        with pytest.raises(SystemExit):
            with pytest.raises(IOError):
                api.get_token()

        monkeypatch.setattr(builtins, "open", self.token_file_good)

        data = api.get_token()
        assert isinstance(data, dict)

    def test_set_token(self, api, monkeypatch):
        monkeypatch.setattr(builtins, "open", self.token_file_good)
        api.set_token("test_string")

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
        monkeypatch.setattr(os.path, "isfile", self.os_path_isfile_true)
        monkeypatch.setattr(builtins, "open", self.token_file_good)
        monkeypatch.setattr(os.path, "isfile", self.os_path_isfile_true)
        monkeypatch.setattr(
            FitbarkApi, "get_authorization_url", self.get_authorization_url
        )
        monkeypatch.setattr(builtins, "input", self.input)
        monkeypatch.setattr(FitbarkApi, "request_token", self.request_token)

        def test_empty():
            main([])

        # def test_help():
        #     main(['-h'])

        def test_arg_get():
            monkeypatch.setattr(FitbarkApi, "hass_get_token", self.hass_get_token)
            monkeypatch.setattr(
                FitbarkApi, "hass_get_redirect_urls", self.hass_get_redirect_urls
            )
            main(["-g"])

        def test_arg_reset():
            monkeypatch.setattr(FitbarkApi, "hass_get_token", self.hass_get_token)
            monkeypatch.setattr(
                FitbarkApi, "hass_add_redirect_urls", self.hass_add_redirect_urls
            )
            main(["-r"])

        def test_arg_add():
            monkeypatch.setattr(FitbarkApi, "hass_get_token", self.hass_get_token)
            monkeypatch.setattr(FitbarkApi, "hass_add_url", self.hass_add_url)
            monkeypatch.setattr(
                FitbarkApi, "hass_get_redirect_urls", self.hass_get_redirect_urls
            )
            main(["-a"])

        def test_arg_remove():
            monkeypatch.setattr(FitbarkApi, "hass_get_token", self.hass_get_token)
            monkeypatch.setattr(FitbarkApi, "hass_remove_url", self.hass_remove_url)
            monkeypatch.setattr(
                FitbarkApi, "hass_get_redirect_urls", self.hass_get_redirect_urls
            )
            main(["-x"])

        def test_arg_user():
            monkeypatch.setattr(FitbarkApi, "get_user_profile", self.get_user_profile)
            main(["-u"])

        def test_arg_user_slug():
            monkeypatch.setattr(FitbarkApi, "get_user_profile", self.get_user_profile)
            main(["--user-slug"])

        def test_arg_user_pic():
            monkeypatch.setattr(FitbarkApi, "get_user_profile", self.get_user_profile)
            monkeypatch.setattr(FitbarkApi, "get_user_picture", self.get_user_picture)
            main(["--user-pic"])

        def test_arg_dogs():
            monkeypatch.setattr(
                FitbarkApi, "get_user_related_dogs", self.get_user_related_dogs
            )
            main(["-d"])

        def test_arg_dog_slug():
            monkeypatch.setattr(
                FitbarkApi, "get_user_related_dogs", self.get_user_related_dogs
            )
            main(["--dog-slug"])

        def test_arg_dog():
            monkeypatch.setattr(
                FitbarkApi, "get_user_related_dogs", self.get_user_related_dogs
            )
            monkeypatch.setattr(FitbarkApi, "get_dog", self.get_dog)
            main(["--dog"])

        def test_arg_dog_pic():
            monkeypatch.setattr(
                FitbarkApi, "get_user_related_dogs", self.get_user_related_dogs
            )
            monkeypatch.setattr(FitbarkApi, "get_dog_picture", self.get_dog_picture)
            main(["--dog-pic"])

        test_empty()
        # test_help():
        test_arg_get()
        test_arg_reset()
        test_arg_add()
        test_arg_remove()
        test_arg_user()
        test_arg_user_slug()
        test_arg_user_pic()
        test_arg_dogs()
        test_arg_dog_slug()
        test_arg_dog()
        test_arg_dog_pic()
