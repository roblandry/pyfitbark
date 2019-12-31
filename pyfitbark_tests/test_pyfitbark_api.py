# -*- coding: utf-8 -*-
"""PyFitBark API Tests."""
import os

import httpretty

import pytest

from pyfitbark.api import BASE_URL, FitbarkApi

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


class TestFitbarkApi:
    """Unit tests for pyfitbark.FitbarkApi."""

    @pytest.fixture
    def api(self):
        """Return MOCK Fitbark API."""
        return FitbarkApi("foo", "faa", "https://whatever.com")

    @httpretty.activate
    def test_get_user_profile(self, api):
        """Test FitbarkApi.get_user_profile()."""
        with open(
            os.path.join(CURRENT_DIR, "json/", "get_user_profile.json"), "r"
        ) as get_user_profile:
            httpretty.register_uri(
                httpretty.GET, BASE_URL + "/user", body=get_user_profile.read()
            )
        data = api.get_user_profile()
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
        slug = "00000000-zzzz-1111-2222-xxxxxxxxxxxx"

        with open(
            os.path.join(CURRENT_DIR, "json/", "get_user_picture.json"), "r"
        ) as get_user_picture:
            httpretty.register_uri(
                httpretty.GET,
                BASE_URL + "/picture/user/" + slug,
                body=get_user_picture.read(),
            )
        data = api.get_user_picture(slug)
        assert len(data) == 1
        image = data["image"]
        assert len(image) == 1
        assert image["data"] == "/9j/4AAQSkZJRgABAQAASABIAAD/4QBYRXhpZgAATU0AKgAAAA"

    @httpretty.activate
    def test_get_user_related_dogs(self, api):
        """Test FitbarkApi.get_user_related_dogs()."""
        with open(
            os.path.join(CURRENT_DIR, "json/", "get_user_related_dogs.json"), "r"
        ) as get_user_related_dogs:
            httpretty.register_uri(
                httpretty.GET,
                BASE_URL + "/dog_relations",
                body=get_user_related_dogs.read(),
            )
        data = api.get_user_related_dogs()
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
        slug = "00000000-zzzz-1111-2222-xxxxxxxxxxxx"

        with open(os.path.join(CURRENT_DIR, "json/", "get_dog.json"), "r") as get_dog:
            httpretty.register_uri(
                httpretty.GET, BASE_URL + "/dog/" + slug, body=get_dog.read(),
            )
        data = api.get_dog(slug)
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
        slug = "00000000-zzzz-1111-2222-xxxxxxxxxxxx"

        with open(
            os.path.join(CURRENT_DIR, "json/", "get_dog_picture.json"), "r"
        ) as get_dog_picture:
            httpretty.register_uri(
                httpretty.GET,
                BASE_URL + "/picture/dog/" + slug,
                body=get_dog_picture.read(),
            )
        data = api.get_dog_picture(slug)
        assert len(data) == 1
        image = data["image"]
        assert len(image) == 1
        assert image["data"] == "/9j/4AAQSkZJRgABAQAASABIAAD/4QBYRXhpZgAATU0AKgAAAA"

    @httpretty.activate
    def test_get_dog_related_users(self, api):
        """Test FitbarkApi.get_dog_related_users()."""
        slug = "00000000-zzzz-1111-2222-xxxxxxxxxxxx"

        with open(
            os.path.join(CURRENT_DIR, "json/", "get_dog_related_users.json"), "r"
        ) as get_dog_related_users:
            httpretty.register_uri(
                httpretty.GET,
                BASE_URL + "/user_relations/" + slug,
                body=get_dog_related_users.read(),
            )
        data = api.get_dog_related_users(slug)
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
        slug = "00000000-zzzz-1111-2222-xxxxxxxxxxxx"

        with open(
            os.path.join(CURRENT_DIR, "json/", "get_daily_goal.json"), "r"
        ) as get_daily_goal:
            httpretty.register_uri(
                httpretty.GET,
                BASE_URL + "/daily_goal/" + slug,
                body=get_daily_goal.read(),
            )
        data = api.get_daily_goal(slug)
        assert len(data) == 1
        daily_goals = data["daily_goals"][0]
        assert len(daily_goals) == 2
        assert daily_goals["goal"] == 1091
        assert daily_goals["date"] == "2019-12-31"
