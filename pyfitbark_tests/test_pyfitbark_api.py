import os

import httpretty
import requests

# import mock
import pytest

# from pymfy.api.devices.category import Category
# from pymfy.api.model import Command, Parameter
from pyfitbark.api import BASE_URL, FitbarkApi

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


class TestFitbarkApi:
    @pytest.fixture(scope="class")
    def api(self):
        return FitbarkApi("foo", "faa", "https://whatever.com")

    def test_get_user_profile(self, monkeypatch):
        json = {
            "user": {
                "slug": "00000000-zzzz-1111-2222-xxxxxxxxxxxx",
                "username": "fake1@domain.com",
                "name": "John Smith",
                "first_name": "John",
                "last_name": "Smith",
                "picture_hash": None,
            }
        }

        def mock_get(self, path):
            return json

        monkeypatch.setattr(FitbarkApi, "get", mock_get)
        r = FitbarkApi.get(self, "/user")
        assert r == json

    def test_get_user_picture(self, monkeypatch):
        slug = "00000000-zzzz-1111-2222-xxxxxxxxxxxx"
        json = {"image": {"data": "/9j/4AAQSkZJRgABAQAASABIAAD/4QBYRXhpZgAATU0AKgAAAA"}}

        def mock_get(self, path):
            return json

        monkeypatch.setattr(FitbarkApi, "get", mock_get)
        r = FitbarkApi.get(self, "/picture/user/" + slug)
        assert r == json

    def test_get_user_related_dogs(self, monkeypatch):
        json = {
            "dog_relations": [
                {
                    "id": 8836,
                    "status": "OWNER",
                    "date": "2016-02-08T22:15:58.000Z",
                    "dog": {
                        "slug": "21d131d5-9616-4e95-bbb2-02c631ef4268",
                        "name": "Bingle",
                        "bluetooth_id": "f00eb7ce3c26",
                        "activity_value": 1123,
                        "activity_date": "2019-12-27T16:47:18.000Z",
                        "birth": "2015-02-08",
                        "breed1": {"id": 392, "name": "Pig", "not_a_dog": True},
                        "breed2": {"id": 224, "name": "Cairn Terrier"},
                        "gender": "M",
                        "weight": 5,
                        "weight_unit": "lbs",
                        "country": "US",
                        "zip": "64108",
                        "tzoffset": -21600,
                        "tzname": "America/Chicago",
                        "min_play": 4,
                        "min_active": 158,
                        "min_rest": 438,
                        "medical_conditions": [],
                        "hourly_average": 112,
                        "picture_hash": "",
                        "neutered": False,
                        "last_min_time": "2019-12-27T09:59:00.000Z",
                        "last_min_activity": 0,
                        "daily_goal": 11900,
                        "battery_level": 0,
                        "description": None,
                    },
                }
            ]
        }

        def mock_get(self, path):
            return json

        monkeypatch.setattr(FitbarkApi, "get", mock_get)
        r = FitbarkApi.get(self, "/dog_relations")
        assert r == json

    def test_get_dog(self, monkeypatch):
        slug = "00000000-zzzz-1111-2222-xxxxxxxxxxxx"
        json = {
            "dog": {
                "slug": "036aa64a-96cc-4fec-bee9-2e3c843208a0",
                "name": "Rose",
                "bluetooth_id": "f00ebadd5ca3",
                "activity_value": 0,
                "birth": "2015-02-08",
                "breed1": {"id": 229, "name": "Chesapeake Bay Retriever"},
                "breed2": {"id": 187, "name": "American Foxhound"},
                "gender": "F",
                "weight": 80,
                "weight_unit": "lbs",
                "country": "US",
                "zip": "64108",
                "tzoffset": -21600,
                "tzname": "America/Chicago",
                "min_play": 0,
                "min_active": 0,
                "min_rest": 0,
                "medical_conditions": [
                    {"id": 7, "name": "Overweight", "description": ""}
                ],
                "hourly_average": 0,
                "picture_hash": "c8ba24128de5e2e2631b74ee1f2cb5ba",
                "neutered": True,
                "last_min_time": "2019-12-30T22:59:00.000Z",
                "last_min_activity": 0,
                "daily_goal": 1091,
                "battery_level": 0,
                "description": None,
                "last_sync": "2019-12-31T05:47:21.000Z",
            }
        }

        def mock_get(self, path):
            return json

        monkeypatch.setattr(FitbarkApi, "get", mock_get)
        r = FitbarkApi.get(self, "/dog/" + slug)
        assert r == json

    def test_get_dog_picture(self, monkeypatch):
        slug = "00000000-zzzz-1111-2222-xxxxxxxxxxxx"
        json = {"image": {"data": "/9j/4AAQSkZJRgABAQAASABIAAD/4QBYRXhpZgAATU0AKgAAAA"}}

        def mock_get(self, path):
            return json

        monkeypatch.setattr(FitbarkApi, "get", mock_get)
        r = FitbarkApi.get(self, "/picture/dog/" + slug)
        assert r == json

    def test_get_dog_related_users(self, monkeypatch):
        slug = "00000000-zzzz-1111-2222-xxxxxxxxxxxx"
        json = {
            "user_relation": [
                {
                    "id": 8836,
                    "date": "2016-02-08T22:15:58.000Z",
                    "dog_slug": "21d131d5-9616-4e95-bbb2-02c631ef4268",
                    "status": "OWNER",
                    "user": {
                        "slug": "9b4ed51b-81cc-473d-9a41-729418f7f963",
                        "username": "fake_001@fitbark.com",
                        "name": "John Smith",
                        "first_name": "John",
                        "last_name": "Smith",
                    },
                }
            ]
        }

        def mock_get(self, path):
            return json

        monkeypatch.setattr(FitbarkApi, "get", mock_get)
        r = FitbarkApi.get(self, "/user_relations/" + slug)
        assert r == json

    def test_get_daily_goal(self, monkeypatch):
        slug = "00000000-zzzz-1111-2222-xxxxxxxxxxxx"
        json = {"daily_goals": [{"goal": 1091, "date": "2019-12-31"}]}

        def mock_get(self, path):
            return json

        monkeypatch.setattr(FitbarkApi, "get", mock_get)
        r = FitbarkApi.get(self, "/daily_goal/" + slug)
        assert r == json
