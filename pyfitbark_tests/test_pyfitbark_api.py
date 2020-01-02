# -*- coding: utf-8 -*-
"""PyFitBark API Tests."""
import os

import httpretty

import pytest

import datetime

import json

from requests_oauthlib import OAuth2Session

from pyfitbark.api import BASE_URL, FitbarkApi

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SLUG = "09659a8a-24c9-4246-92a8-7ecd0650368c"
ACCESS_TOKEN = "DCEOB729f3i5CuLCyZCkX_5slG_fpc1IhNqf0FnfK_YDmmc7bZ"


class MockResponse:
    @staticmethod
    def oauth_fetch_token():
        return {"mock_key": "mock_response"}

    @staticmethod
    def oauth_refresh_token():
        return {"mock_key": "mock_response"}

    @staticmethod
    def get_dict():
        return {"mock_key": "mock_response"}

    @staticmethod
    def get_list():
        return ["mock_response_1", "mock_response_2"]

    @staticmethod
    def get_redirect_urls():
        return ["http://mock_url.com/auth/external/callback"]

    @staticmethod
    def get_from_file(file):
        file_data = open(os.path.join(CURRENT_DIR, "json/", f"{file}.json"), "r")
        data = json.loads(file_data.read())
        return data


class TestFitbarkApi:
    """Unit tests for pyfitbark.FitbarkApi."""

    @pytest.fixture
    def api(self):
        """Return MOCK Fitbark API."""
        return FitbarkApi(
            "foo", "faa", "https://whatever.com", None, None, "http://mock_url.com"
        )

    def hass_get_token(self, *args, **kwargs):  # pylint: disable=unused-argument
        return MockResponse.get_from_file("hass_get_token")

    def hass_get_redirect_urls(
        self, *args, **kwargs
    ):  # pylint: disable=unused-argument
        return MockResponse.get_redirect_urls()

    def hass_add_redirect_urls(
        self, *args, **kwargs
    ):  # pylint: disable=unused-argument
        return MockResponse.get_dict()

    def hass_make_request(self, *args, **kwargs):  # pylint: disable=unused-argument
        return MockResponse.get_from_file("hass_get_token")

    def hass_add_url(self, *args, **kwargs):  # pylint: disable=unused-argument
        return None

    def hass_remove_url(self, *args, **kwargs):  # pylint: disable=unused-argument
        return None

    def mock_fetch_token(self, *args, **kwargs):  # pylint: disable=unused-argument
        return MockResponse.oauth_fetch_token()

    def mock_refresh_token(self, *args, **kwargs):  # pylint: disable=unused-argument
        return MockResponse.oauth_refresh_token()

    def open_file(self, file, method, url):
        """Open file and register httpretty uri."""
        with open(os.path.join(CURRENT_DIR, "json/", f"{file}.json"), "r") as o_file:
            httpretty.register_uri(method, f"{BASE_URL}{url}", body=o_file.read())

    @httpretty.activate
    def test_get_user_profile(self, api):
        """Test FitbarkApi.get_user_profile()."""
        self.open_file("get_user_profile", httpretty.GET, "/user")

        data = api.get_user_profile()
        assert isinstance(data, dict)
        assert len(data) == 1
        user = data["user"]
        assert len(user) == 6
        assert user["slug"] == "00000000-zzzz-1111-2222-xxxxxxxxxxxx"
        assert user["username"] == "fake1@domain.com"
        assert user["name"] == "John Smith"
        assert user["first_name"] == "John"
        assert user["last_name"] == "Smith"
        assert user["picture_hash"] == "fdszgxcfkhgjlbnm"

    @httpretty.activate
    def test_get_user_picture(self, api):
        """Test FitbarkApi.get_user_picture()."""
        self.open_file("get_user_picture", httpretty.GET, f"/picture/user/{SLUG}")

        data = api.get_user_picture(SLUG)
        assert isinstance(data, dict)
        assert len(data) == 1
        image = data["image"]
        assert len(image) == 1
        assert image["data"] == "/9j/4AAQSkZJRgABAQAASABIAAD/4QBYRXhpZgAATU0AKgAAAA"

    @httpretty.activate
    def test_get_user_related_dogs(self, api):
        """Test FitbarkApi.get_user_related_dogs()."""
        self.open_file("get_user_related_dogs", httpretty.GET, "/dog_relations")

        data = api.get_user_related_dogs()
        assert isinstance(data, dict)
        assert len(data) == 1
        dog_relations = data["dog_relations"]
        assert len(dog_relations[0]) == 4
        assert dog_relations[0]["id"] == 8836
        assert dog_relations[0]["status"] == "OWNER"
        assert dog_relations[0]["date"] == "2016-02-08T22:15:58.000Z"
        dog_relations_dog = dog_relations[0]["dog"]
        assert len(dog_relations_dog) == 27
        assert dog_relations_dog["slug"] == "21d131d5-9616-4e95-bbb2-02c631ef4268"
        assert dog_relations_dog["name"] == "Bingle"
        assert dog_relations_dog["bluetooth_id"] == "f00eb7ce3c26"
        assert dog_relations_dog["activity_value"] == 1123
        assert dog_relations_dog["activity_date"] == "2019-12-27T16:47:18.000Z"
        assert dog_relations_dog["birth"] == "2015-02-08"
        assert dog_relations_dog["breed1"] == {
            "id": 392,
            "name": "Pig",
            "not_a_dog": "True",
        }
        assert dog_relations_dog["breed2"] == {"id": 224, "name": "Cairn Terrier"}
        assert dog_relations_dog["gender"] == "M"
        assert dog_relations_dog["weight"] == 5
        assert dog_relations_dog["weight_unit"] == "lbs"
        assert dog_relations_dog["country"] == "US"
        assert dog_relations_dog["zip"] == "64108"
        assert dog_relations_dog["tzoffset"] == -21600
        assert dog_relations_dog["tzname"] == "America/Chicago"
        assert dog_relations_dog["min_play"] == 4
        assert dog_relations_dog["min_active"] == 158
        assert dog_relations_dog["min_rest"] == 438
        assert dog_relations_dog["medical_conditions"] == []
        assert dog_relations_dog["hourly_average"] == 112
        assert dog_relations_dog["picture_hash"] == ""
        assert dog_relations_dog["neutered"] == "False"
        assert dog_relations_dog["last_min_time"] == "2019-12-27T09:59:00.000Z"
        assert dog_relations_dog["last_min_activity"] == 0
        assert dog_relations_dog["daily_goal"] == 11900
        assert dog_relations_dog["battery_level"] == 0
        assert dog_relations_dog["description"] == "None"

    @httpretty.activate
    def test_get_dog(self, api):
        """Test FitbarkApi.get_dog()."""
        self.open_file("get_dog", httpretty.GET, f"/dog/{SLUG}")

        data = api.get_dog(SLUG)
        assert isinstance(data, dict)
        assert len(data) == 1
        dog = data["dog"]
        assert len(dog) == 27
        assert dog["slug"] == "036aa64a-96cc-4fec-bee9-2e3c843208a0"
        assert dog["name"] == "Rose"
        assert dog["bluetooth_id"] == "f00ebadd5ca3"
        assert dog["activity_value"] == 0
        # assert dog["activity_date"] == "2019-12-27T16:47:18.000Z"
        assert dog["birth"] == "2015-02-08"
        assert dog["breed1"] == {"id": 229, "name": "Chesapeake Bay Retriever"}
        assert dog["breed2"] == {"id": 187, "name": "American Foxhound"}
        assert dog["gender"] == "F"
        assert dog["weight"] == 80
        assert dog["weight_unit"] == "lbs"
        assert dog["country"] == "US"
        assert dog["zip"] == "64108"
        assert dog["tzoffset"] == -21600
        assert dog["tzname"] == "America/Chicago"
        assert dog["min_play"] == 0
        assert dog["min_active"] == 0
        assert dog["min_rest"] == 0
        assert dog["medical_conditions"] == [
            {"id": 7, "name": "Overweight", "description": ""}
        ]
        assert dog["hourly_average"] == 0
        assert dog["picture_hash"] == "c8ba24128de5e2e2631b74ee1f2cb5ba"
        assert dog["neutered"] == "True"
        assert dog["last_min_time"] == "2019-12-30T22:59:00.000Z"
        assert dog["last_min_activity"] == 0
        assert dog["daily_goal"] == 1091
        assert dog["battery_level"] == 0
        assert dog["description"] == "None"
        assert dog["last_sync"] == "2019-12-31T05:47:21.000Z"

    @httpretty.activate
    def test_get_dog_picture(self, api):
        """Test FitbarkApi.get_dog_picture()."""
        self.open_file("get_dog_picture", httpretty.GET, f"/picture/dog/{SLUG}")

        data = api.get_dog_picture(SLUG)
        assert isinstance(data, dict)
        assert len(data) == 1
        image = data["image"]
        assert len(image) == 1
        assert image["data"] == "/9j/4AAQSkZJRgABAQAASABIAAD/4QBYRXhpZgAATU0AKgAAAA"

    @httpretty.activate
    def test_get_dog_related_users(self, api):
        """Test FitbarkApi.get_dog_related_users()."""
        self.open_file(
            "get_dog_related_users", httpretty.GET, f"/user_relations/{SLUG}"
        )

        data = api.get_dog_related_users(SLUG)
        assert isinstance(data, dict)
        assert len(data) == 1
        user_relation = data["user_relation"][0]
        assert len(user_relation) == 5
        assert user_relation["id"] == 8836
        assert user_relation["date"] == "2016-02-08T22:15:58.000Z"
        assert user_relation["dog_slug"] == "21d131d5-9616-4e95-bbb2-02c631ef4268"
        assert user_relation["status"] == "OWNER"
        user = user_relation["user"]
        assert len(user) == 5
        assert user["slug"] == "9b4ed51b-81cc-473d-9a41-729418f7f963"
        assert user["username"] == "fake_001@fitbark.com"
        assert user["name"] == "John Smith"
        assert user["first_name"] == "John"
        assert user["last_name"] == "Smith"

    @httpretty.activate
    def test_get_daily_goal(self, api):
        """Test FitbarkApi.get_daily_goal()."""
        self.open_file("get_daily_goal", httpretty.GET, f"/daily_goal/{SLUG}")

        data = api.get_daily_goal(SLUG)
        assert isinstance(data, dict)
        assert len(data) == 1
        daily_goals = data["daily_goals"][0]
        assert len(daily_goals) == 2
        assert daily_goals["goal"] == 1091
        assert daily_goals["date"] == "2019-12-31"

    @httpretty.activate
    def test_set_daily_goal(self, api):
        """Test FitbarkApi.set_daily_goal()."""
        self.open_file("get_daily_goal", httpretty.PUT, f"/daily_goal/{SLUG}")
        data = {"daily_goal": 7000, "date": "2014-08-15"}

        data = api.set_daily_goal(SLUG, data)
        assert isinstance(data, dict)
        assert len(data) == 1
        daily_goals = data["daily_goals"][0]
        assert len(daily_goals) == 2
        assert daily_goals["goal"] == 1091
        assert daily_goals["date"] == "2019-12-31"

    # # def _build_api_url(self, endpoint):
    # #     return "{0}/v{1}/{endpoint}".format(
    # #         self.API_ENDPOINT, self.API_VERSION, endpoint=endpoint)

    # # def _get_common_args(self):
    # #     return self.API_ENDPOINT, self.API_VERSION

    def test_get_date_string(self, api):
        """Test FitbarkApi._get_date_string()."""
        date = "2019-12-31"
        data = api._get_date_string(date)  # NOQA
        assert isinstance(data, str)
        assert data == "2019-12-31"

        today = datetime.date.today()
        data = api._get_date_string(today)  # NOQA
        assert isinstance(data, str)
        assert data == today.strftime("%Y-%m-%d")

    @httpretty.activate
    def test_get_activity_series(self, api):
        """Test FitbarkApi.get_activity_series()."""

        def verify_return(data):
            assert isinstance(data, dict)
            assert len(data) == 1
            activity_series = data["activity_series"]
            assert len(activity_series) == 2
            assert len(activity_series["records"]) == 2

            records = activity_series["records"][0]
            assert len(records) == 7
            assert records["date"] == "2014-12-27"
            assert records["activity_value"] == 921
            assert records["min_play"] == 15
            assert records["min_active"] == 125
            assert records["min_rest"] == 1300
            assert records["daily_target"] == 5000
            assert records["has_trophy"] == 0

            records = activity_series["records"][1]
            assert len(records) == 7
            assert records["date"] == "2014-12-28"
            assert records["activity_value"] == 5421
            assert records["min_play"] == 114
            assert records["min_active"] == 484
            assert records["min_rest"] == 838
            assert records["daily_target"] == 5000
            assert records["has_trophy"] == 1

        self.open_file("get_activity_series", httpretty.POST, "/activity_series")

        data = api.get_activity_series("/activity_series")
        verify_return(data)

        data = api.get_activity_series(
            "/activity_series", "2019-12-25", "2019-12-31", "BAD INPUT"
        )
        verify_return(data)

        with pytest.raises(ValueError):
            assert api.get_activity_series(
                "/activity_series", "2019-12-31", "2019-12-25"
            )

    @httpretty.activate
    def test_get_dog_similar_stats(self, api):
        """Test FitbarkApi.get_dog_similar_stats()."""
        self.open_file("get_dog_similar_stats", httpretty.POST, "/similar_dogs_stats")

        data = api.get_dog_similar_stats(SLUG)
        assert isinstance(data, dict)
        assert len(data) == 1
        similar_dogs_stats = data["similar_dogs_stats"]
        assert len(similar_dogs_stats) == 10
        assert similar_dogs_stats["this_best_daily_activity"] == 2300
        assert similar_dogs_stats["this_best_week_activity"] == 56000
        assert similar_dogs_stats["this_current_goals_streak"] == 1
        assert similar_dogs_stats["this_best_goals_streak"] == 3
        assert similar_dogs_stats["this_average_daily_activity"] == 2100
        assert similar_dogs_stats["median_same_age_weight_daily_activity"] == 2500
        assert similar_dogs_stats["this_average_daily_rest_minutes"] == 60
        assert (
            similar_dogs_stats["median_same_age_weight_range_dogs_daily_rest_minutes"]
            == 54
        )
        assert similar_dogs_stats["median_all_dogs_daily_activity"] == 3000
        assert similar_dogs_stats["median_same_breed_daily_activity"] == 3500

    @httpretty.activate
    def test_get_activity_totals(self, api):
        """Test FitbarkApi.get_activity_totals()."""

        def verify_return(data):
            assert isinstance(data, dict)
            assert len(data) == 1
            assert data["activity_value"] == 26305

        self.open_file("get_activity_totals", httpretty.POST, "/activity_totals")

        data = api.get_activity_totals("/activity_totals")
        verify_return(data)

        data = api.get_activity_totals("/activity_totals", "2019-12-25", "2019-12-31")
        verify_return(data)

        with pytest.raises(ValueError):
            assert api.get_activity_totals(
                "/activity_totals", "2019-12-31", "2019-12-25"
            )

    @httpretty.activate
    def test_get_time_breakdown(self, api):
        """Test FitbarkApi.get_time_breakdown()."""

        def verify_return(data):
            assert isinstance(data, dict)
            assert len(data) == 1
            activity_level = data["activity_level"]
            assert activity_level["min_play"] == 321
            assert activity_level["min_active"] == 941
            assert activity_level["min_rest"] == 4498

        self.open_file("get_time_breakdown", httpretty.POST, "/time_breakdown")

        data = api.get_time_breakdown("/time_breakdown")
        verify_return(data)

        data = api.get_time_breakdown("/time_breakdown", "2019-12-25", "2019-12-31")
        verify_return(data)

        with pytest.raises(ValueError):
            assert api.get_time_breakdown("/time_breakdown", "2019-12-31", "2019-12-25")

    @httpretty.activate
    def test_get(self, api):
        """Test FitbarkApi.get()."""
        self.open_file("get_dog_picture", httpretty.GET, f"/picture/dog/{SLUG}")

        data = api.get("/picture/dog/" + SLUG)
        # assert isinstance(data, Response)
        data = data.json()
        assert isinstance(data, dict)
        assert len(data) == 1
        image = data["image"]
        assert len(image) == 1
        assert image["data"] == "/9j/4AAQSkZJRgABAQAASABIAAD/4QBYRXhpZgAATU0AKgAAAA"

    @httpretty.activate
    def test_post(self, api):
        """Test FitbarkApi.post()."""
        self.open_file("get_time_breakdown", httpretty.POST, "/time_breakdown")

        data = api.post(
            "/time_breakdown",
            json={
                "dog": {
                    "slug": "09659a8a-24c9-4246-92a8-7ecd0650368c",
                    "from": "2019-12-25",
                    "to": "2019-12-31",
                }
            },
        )
        # assert isinstance(data, Response)
        data = data.json()
        assert isinstance(data, dict)
        assert len(data) == 1
        activity_level = data["activity_level"]
        assert activity_level["min_play"] == 321
        assert activity_level["min_active"] == 941
        assert activity_level["min_rest"] == 4498

    @httpretty.activate
    def test_put(self, api):
        """Test FitbarkApi.put()."""
        self.open_file("get_daily_goal", httpretty.PUT, f"/daily_goal/{SLUG}")

        data = api.put(
            "/daily_goal/" + SLUG, json={"daily_goal": 7000, "date": "2014-08-15"}
        )
        # assert isinstance(data, Response)
        data = data.json()
        assert isinstance(data, dict)
        assert len(data) == 1
        daily_goals = data["daily_goals"][0]
        assert len(daily_goals) == 2
        assert daily_goals["goal"] == 1091
        assert daily_goals["date"] == "2019-12-31"

    def test_get_authorization_url(self, api):
        """Test FitbarkApi.get_authorization_url()."""
        assert isinstance(api.get_authorization_url(), tuple)

    def test_request_token(self, api, monkeypatch):
        """Test FitbarkApi.request_token()."""
        monkeypatch.setattr(OAuth2Session, "fetch_token", self.mock_fetch_token)
        # A OAuth2Token object (a dict too).
        assert isinstance(
            api.request_token("fake authorization_response", "fake code"), dict
        )

    def test_refresh_tokens(self, api, monkeypatch):
        """Test FitbarkApi.refresh_tokens()."""
        monkeypatch.setattr(OAuth2Session, "refresh_token", self.mock_refresh_token)

        assert isinstance(api.refresh_tokens(), dict)

    # @httpretty.activate
    # def test_request(self, api, monkeypatch):
    #     """Test FitbarkApi._request()."""
    #     monkeypatch.setattr(OAuth2Session, "get", self.mock_get)
    #     except TokenExpiredError
    #     self.refresh_tokens

    def test_hass_add_url(self, api, monkeypatch):
        """Test FitbarkApi.hass_add_url()."""
        monkeypatch.setattr(api, "hass_get_token", self.hass_get_token)
        monkeypatch.setattr(api, "hass_get_redirect_urls", self.hass_get_redirect_urls)
        monkeypatch.setattr(api, "hass_add_redirect_urls", self.hass_add_redirect_urls)

        # api._callback_url = "http://mock_url.com"  # pylint: disable=protected-access
        api.hass_add_url()

    def test_hass_remove_url(self, api, monkeypatch):
        """Test FitbarkApi.hass_remove_url()."""
        monkeypatch.setattr(api, "hass_get_token", self.hass_get_token)
        monkeypatch.setattr(api, "hass_get_redirect_urls", self.hass_get_redirect_urls)
        monkeypatch.setattr(api, "hass_add_redirect_urls", self.hass_add_redirect_urls)

        # api._callback_url = "http://mock_url.com"  # pylint: disable=protected-access
        api.hass_remove_url()

    # @httpretty.activate
    # def test_hass_make_request(self, api, monkeypatch):
    #     """Test FitbarkApi.hass_make_request()."""

    def test_hass_get_token(self, api, monkeypatch):
        """Test FitbarkApi.hass_get_token()."""
        monkeypatch.setattr(api, "hass_make_request", self.hass_make_request)

        data = api.hass_get_token()
        assert isinstance(data, str)
        assert (
            data
            == "db73736bc5713e986415fd22345678e2a1f0d8f84eefee3d78515b643db329c341679"
        )

    @httpretty.activate
    def test_hass_get_redirect_urls(self, api):
        """Test FitbarkApi.hass_get_redirect_urls()."""
        httpretty.register_uri(
            httpretty.GET,
            BASE_URL + "/redirect_urls",
            body='{"redirect_uri": "urn:ietf:wg:oauth:2.0:oob"}',
        )
        data = api.hass_get_redirect_urls(ACCESS_TOKEN)
        assert isinstance(data, list)
        assert data == ["urn:ietf:wg:oauth:2.0:oob"]

    @httpretty.activate
    def test_hass_add_redirect_urls(self, api):
        """Test FitbarkApi.hass_add_redirect_urls()."""
        httpretty.register_uri(
            httpretty.POST,
            BASE_URL + "/redirect_urls",
            body='{"redirect_uri": "urn:ietf:wg:oauth:2.0:oob"}',
        )
        data = api.hass_add_redirect_urls("urn:ietf:wg:oauth:2.0:oob", ACCESS_TOKEN)
        assert isinstance(data, dict)
        assert len(data) == 1
        assert data["redirect_uri"] == "urn:ietf:wg:oauth:2.0:oob"
