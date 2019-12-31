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
        slug = "09659a8a-24c9-4246-92a8-7ecd0650368c"

        with open(
            os.path.join(CURRENT_DIR, "json/", "get_user_picture.json"), "r"
        ) as get_user_picture:
            httpretty.register_uri(
                httpretty.GET,
                BASE_URL + "/picture/user/" + slug,
                body=get_user_picture.read(),
            )
        data = api.get_user_picture(slug)
        assert isinstance(data, dict)
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
        slug = "09659a8a-24c9-4246-92a8-7ecd0650368c"

        with open(os.path.join(CURRENT_DIR, "json/", "get_dog.json"), "r") as get_dog:
            httpretty.register_uri(
                httpretty.GET, BASE_URL + "/dog/" + slug, body=get_dog.read(),
            )
        data = api.get_dog(slug)
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
        slug = "09659a8a-24c9-4246-92a8-7ecd0650368c"

        with open(
            os.path.join(CURRENT_DIR, "json/", "get_dog_picture.json"), "r"
        ) as get_dog_picture:
            httpretty.register_uri(
                httpretty.GET,
                BASE_URL + "/picture/dog/" + slug,
                body=get_dog_picture.read(),
            )
        data = api.get_dog_picture(slug)
        assert isinstance(data, dict)
        assert len(data) == 1
        image = data["image"]
        assert len(image) == 1
        assert image["data"] == "/9j/4AAQSkZJRgABAQAASABIAAD/4QBYRXhpZgAATU0AKgAAAA"

    @httpretty.activate
    def test_get_dog_related_users(self, api):
        """Test FitbarkApi.get_dog_related_users()."""
        slug = "09659a8a-24c9-4246-92a8-7ecd0650368c"

        with open(
            os.path.join(CURRENT_DIR, "json/", "get_dog_related_users.json"), "r"
        ) as get_dog_related_users:
            httpretty.register_uri(
                httpretty.GET,
                BASE_URL + "/user_relations/" + slug,
                body=get_dog_related_users.read(),
            )
        data = api.get_dog_related_users(slug)
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
        slug = "09659a8a-24c9-4246-92a8-7ecd0650368c"

        with open(
            os.path.join(CURRENT_DIR, "json/", "get_daily_goal.json"), "r"
        ) as get_daily_goal:
            httpretty.register_uri(
                httpretty.GET,
                BASE_URL + "/daily_goal/" + slug,
                body=get_daily_goal.read(),
            )
        data = api.get_daily_goal(slug)
        assert isinstance(data, dict)
        assert len(data) == 1
        daily_goals = data["daily_goals"][0]
        assert len(daily_goals) == 2
        assert daily_goals["goal"] == 1091
        assert daily_goals["date"] == "2019-12-31"

    @httpretty.activate
    def test_set_daily_goal(self, api):
        """Test FitbarkApi.set_daily_goal()."""
        slug = "09659a8a-24c9-4246-92a8-7ecd0650368c"
        data = {"daily_goal": 7000, "date": "2014-08-15"}
        with open(
            os.path.join(CURRENT_DIR, "json/", "get_daily_goal.json"), "r"
        ) as get_daily_goal:
            httpretty.register_uri(
                httpretty.PUT,
                BASE_URL + "/daily_goal/" + slug,
                body=get_daily_goal.read(),
            )
        data = api.set_daily_goal(slug, data)
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

    # @httpretty.activate
    def test_get_date_string(self, api):
        """Test FitbarkApi._get_date_string()."""
        date = "2019-12-31"
        data = api._get_date_string(date)  # NOQA
        assert isinstance(data, str)
        assert data == "2019-12-31"

    @httpretty.activate
    def test_get_activity_series(self, api):
        """Test FitbarkApi.get_activity_series()."""
        with open(
            os.path.join(CURRENT_DIR, "json/", "get_activity_series.json"), "r"
        ) as get_activity_series:
            httpretty.register_uri(
                httpretty.POST,
                BASE_URL + "/activity_series",
                body=get_activity_series.read(),
            )
        data = api.get_activity_series(
            "/activity_series", "2019-12-25", "2019-12-31", "DAILY"
        )
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

    @httpretty.activate
    def test_get_dog_similar_stats(self, api):
        """Test FitbarkApi.get_dog_similar_stats()."""
        slug = "09659a8a-24c9-4246-92a8-7ecd0650368c"

        with open(
            os.path.join(CURRENT_DIR, "json/", "get_dog_similar_stats.json"), "r"
        ) as get_dog_similar_stats:
            httpretty.register_uri(
                httpretty.POST,
                BASE_URL + "/similar_dogs_stats",
                body=get_dog_similar_stats.read(),
            )
        data = api.get_dog_similar_stats(slug)
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
        with open(
            os.path.join(CURRENT_DIR, "json/", "get_activity_totals.json"), "r"
        ) as get_activity_totals:
            httpretty.register_uri(
                httpretty.POST,
                BASE_URL + "/activity_totals",
                body=get_activity_totals.read(),
            )
        data = api.get_activity_totals("/activity_totals", "2019-12-25", "2019-12-31")
        assert isinstance(data, dict)
        assert len(data) == 1
        assert data["activity_value"] == 26305

    @httpretty.activate
    def test_get_time_breakdown(self, api):
        """Test FitbarkApi.get_time_breakdown()."""
        with open(
            os.path.join(CURRENT_DIR, "json/", "get_time_breakdown.json"), "r"
        ) as get_time_breakdown:
            httpretty.register_uri(
                httpretty.POST,
                BASE_URL + "/time_breakdown",
                body=get_time_breakdown.read(),
            )
        data = api.get_time_breakdown("/time_breakdown", "2019-12-25", "2019-12-31")
        assert isinstance(data, dict)
        assert len(data) == 1
        activity_level = data["activity_level"]
        assert activity_level["min_play"] == 321
        assert activity_level["min_active"] == 941
        assert activity_level["min_rest"] == 4498

    @httpretty.activate
    def test_get(self, api):
        """Test FitbarkApi.get()."""
        slug = "09659a8a-24c9-4246-92a8-7ecd0650368c"
        with open(
            os.path.join(CURRENT_DIR, "json/", "get_dog_picture.json"), "r"
        ) as get_dog_picture:
            httpretty.register_uri(
                httpretty.GET,
                BASE_URL + "/picture/dog/" + slug,
                body=get_dog_picture.read(),
            )
        data = api.get("/picture/dog/" + slug)
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
        with open(
            os.path.join(CURRENT_DIR, "json/", "get_time_breakdown.json"), "r"
        ) as get_time_breakdown:
            httpretty.register_uri(
                httpretty.POST,
                BASE_URL + "/time_breakdown",
                body=get_time_breakdown.read(),
            )
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
        slug = "09659a8a-24c9-4246-92a8-7ecd0650368c"
        with open(
            os.path.join(CURRENT_DIR, "json/", "get_daily_goal.json"), "r"
        ) as get_daily_goal:
            httpretty.register_uri(
                httpretty.PUT,
                BASE_URL + "/daily_goal/" + slug,
                body=get_daily_goal.read(),
            )
        data = api.put(
            "/daily_goal/" + slug, json={"daily_goal": 7000, "date": "2014-08-15"}
        )
        # assert isinstance(data, Response)
        data = data.json()
        assert isinstance(data, dict)
        assert len(data) == 1
        daily_goals = data["daily_goals"][0]
        assert len(daily_goals) == 2
        assert daily_goals["goal"] == 1091
        assert daily_goals["date"] == "2019-12-31"

    # @httpretty.activate
    # def test_get_authorization_url(self, api):
    #     """Test FitbarkApi.get_authorization_url()."""
    #     return self._oauth.authorization_url(FITBARK_OAUTH, state)

    # @httpretty.activate
    # def test_request_token(self, api):
    #     """Test FitbarkApi.request_token()."""
    # def request_token(
    #     self, authorization_response: Optional[str] = None, code: Optional[str] = None
    # ) -> Dict[str, str]:
    #     """Generic method to fetch a Fitbark access token.

    #     :param authorization_response: Authorization response URL, the callback
    #                                    URL of the request back to you.
    #     :param code: Authorization code
    #     :return: A token dict
    #     """
    #     return self._oauth.fetch_token(
    #         FITBARK_TOKEN,
    #         authorization_response=authorization_response,
    #         code=code,
    #         client_secret=self.client_secret,
    #     )

    # @httpretty.activate
    # def test_refresh_tokens(self, api):
    #     """Test FitbarkApi.get_daily_goal()."""
    # def refresh_tokens(self) -> Dict[str, Union[str, int]]:
    #     """Refresh and return new Fitbark tokens."""
    #     token = self._oauth.refresh_token(FITBARK_REFRESH)

    #     if self.token_updater is not None:
    #         self.token_updater(token)

    #     return token

    # @httpretty.activate
    # def test__request(self, api):
    #     """Test FitbarkApi.get_daily_goal()."""
    # def _request(self, method: str, path: str, **kwargs: Any) -> Response:
    #     """Make a request.

    #     We don't use the built-in token refresh mechanism of OAuth2 session because
    #     we want to allow overriding the token refresh logic.
    #     """
    #     url = BASE_URL + path

    #     try:
    #         return getattr(self._oauth, method)(url, **kwargs)
    #     except TokenExpiredError:
    #         self._oauth.token = self.refresh_tokens()

    #         return getattr(self._oauth, method)(url, **kwargs)

    # @httpretty.activate
    # def test_(self, api):
    #     """Test FitbarkApi.get_daily_goal()."""
    # def hass_add_url(self) -> None:
    #     """Add callback url for auth."""
    #     if self._callback_url:
    #         callback_url = self._callback_url + "/auth/external/callback"
    #         self.access_token = self.hass_get_token()
    #         redirect_uri = self.hass_get_redirect_urls()
    #         if callback_url not in redirect_uri:
    #             redirect_uri = redirect_uri + "\r" + callback_url
    #             self.hass_add_redirect_urls(redirect_uri)
    #             _LOGGER.debug("Added %s redirect url", callback_url)

    # @httpretty.activate
    # def test_(self, api):
    #     """Test FitbarkApi.get_daily_goal()."""
    # def hass_remove_url(self) -> None:
    #     """Remove the callback url for auth."""
    #     if self._callback_url:
    #         callback_url = self._callback_url + "/auth/external/callback"
    #         self.access_token = self.hass_get_token()
    #         redirect_uri = self.hass_get_redirect_urls()
    #         if callback_url in redirect_uri:
    #             redirect_uri = redirect_uri.replace("\r" + callback_url, "")
    #             self.hass_add_redirect_urls(redirect_uri)
    #             _LOGGER.debug("Removed %s redirect url", callback_url)

    # @httpretty.activate
    # def test_(self, api):
    #     """Test FitbarkApi.get_daily_goal()."""
    # def hass_make_request(
    #     self, method: str, url: str, payload: Dict[str, str], headers: Dict[str, str]
    # ) -> Dict[str, str]:
    #     """Simple request wrapper."""
    #     response = requests.request(method, url, json=payload, headers=headers)

    #     json_data = json.loads(response.text)
    #     # print(json_data)
    #     return json_data

    # @httpretty.activate
    # def test_(self, api):
    #     """Test FitbarkApi.get_daily_goal()."""
    # def hass_get_token(self) -> str:
    #     """Get the token."""
    #     url = "https://app.fitbark.com/oauth/token"
    #     payload = {
    #         "grant_type": "client_credentials",
    #         "client_id": self.client_id,
    #         "client_secret": self.client_secret,
    #         "scope": "fitbark_open_api_2745H78RVS",
    #     }
    #     headers = {"Content-Type": "application/json", "Cache-Control": "no-cache"}

    #     json_data = self.hass_make_request("POST", url, payload, headers)
    #     access_token = json_data["access_token"]
    #     return access_token

    # @httpretty.activate
    # def test_(self, api):
    #     """Test FitbarkApi.get_daily_goal()."""
    # def hass_get_redirect_urls(self) -> str:
    #     """Get a list of redirect URLs."""
    #     url = "https://app.fitbark.com/api/v2/redirect_urls"
    #     payload: Dict[str, str] = {}
    #     headers = {"Authorization": "Bearer " + self.access_token}
    #     json_data = self.hass_make_request("GET", url, payload, headers)
    #     redirect_uri = json_data["redirect_uri"]
    #     return redirect_uri

    # @httpretty.activate
    # def test_(self, api):
    #     """Test FitbarkApi.get_daily_goal()."""
    # def hass_add_redirect_urls(self, redirect_uri: str) -> Dict[str, str]:
    #     """Add the redirect url."""
    #     url = "https://app.fitbark.com/api/v2/redirect_urls"
    #     payload = {"redirect_uri": redirect_uri}
    #     headers = {"Authorization": "Bearer " + self.access_token}
    #     json_data = self.hass_make_request("POST", url, payload, headers)
    #     return json_data
