# -*- coding: utf-8 -*-
"""PyFitBark API.

Code pieces borrowed from python-fitbark and pymfy.

Source: https://github.com/alexhouse/python-fitbark
        https://github.com/tetienne/somfy-open-api
"""
import datetime

# from dateutil.parser import parse
import json
import logging

import requests

# pylint: disable=unused-import
from typing import Tuple, List, Optional, Union, Callable, Dict, Any  # NOQA

from requests import Response
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import TokenExpiredError

_LOGGER = logging.getLogger(__name__)

API_VERSION = "2"
BASE_URL = "https://app.fitbark.com/api/v" + API_VERSION
FITBARK_OAUTH = "https://app.fitbark.com/oauth/authorize"
FITBARK_TOKEN = "https://app.fitbark.com/oauth/token"
FITBARK_REFRESH = "https://app.fitbark.com/oauth/token"
WEEK_DAYS = [
    "SUNDAY",
    "MONDAY",
    "TUESDAY",
    "WEDNESDAY",
    "THURSDAY",
    "FRIDAY",
    "SATURDAY",
]
PERIODS = ["1d", "7d", "30d", "1w", "1m", "3m", "6m", "1y", "max"]


class FitbarkApi:
    """FitBark API implimentation."""

    def __init__(  # pylint: disable=too-many-arguments
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: Optional[str] = None,
        token: Optional[Dict[str, str]] = None,
        token_updater: Optional[Callable[[str], None]] = None,
        callback_url: Optional[str] = None,
    ):
        """Init."""
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_updater = token_updater
        self._callback_url = callback_url

        extra = {"client_id": self.client_id, "client_secret": self.client_secret}

        self._oauth = OAuth2Session(
            client_id=client_id,
            token=token,
            redirect_uri=redirect_uri,
            auto_refresh_kwargs=extra,
            token_updater=token_updater,
        )

    def get_user_profile(self) -> Dict[str, str]:
        """Get various information about the specified user.

        This including name, username (email address), profile picture and Facebook ID.

        :return: user details
        :rtype: json
        """
        r = self.get("/user")
        r.raise_for_status()
        return r.json()

    def get_user_picture(self, slug: str) -> Dict[str, str]:
        """
        Get the Base64 encoded picture for a specified user.

        :param slug: uuid of the user to look up
        :type slug: uuid
        :return: base64 encoded string of image
        :rtype: json
        """
        r = self.get("/picture/user/" + slug)
        r.raise_for_status()
        return r.json()

    def get_user_related_dogs(self) -> Dict[str, str]:
        """
        Get the dogs related to the logged in user.

        :return: list of dogs
        :rtype: json
        """
        r = self.get("/dog_relations")
        r.raise_for_status()
        return r.json()

    def get_dog(self, slug: str) -> Dict[str, str]:
        """
        Get various information about a certain dog.

        This including name, breed, gender, weight, birthday and picture.

        :param slug: uuid of the dog to look up
        :type slug: uuid
        :return: dog's info
        :rtype: json
        """
        r = self.get("/dog/" + slug)
        r.raise_for_status()
        return r.json()

    def get_dog_picture(self, slug: str) -> Dict[str, str]:
        """Get the Base64 encoded picture for a specified dog.

        :param slug: uuid of the dog to return
        :type slug: uuid
        :return: base64 encoded string of image
        :rtype: json
        """
        r = self.get("/picture/dog/" + slug)
        r.raise_for_status()
        return r.json()

    def get_dog_related_users(self, slug: str) -> Dict[str, str]:
        """Get a list of users currently associated with a specified dog.

        Additionally gets the type of relationship (Owner or Friend) and privacy
        settings for each user (how far back in time the activity data is visible).

        :param slug: uuid of the dog to look up
        :type slug: uuid
        :return: list of users
        :rtype: json
        """
        r = self.get("/user_relations/" + slug)
        r.raise_for_status()
        return r.json()

    def get_daily_goal(self, slug: str) -> Dict[str, str]:
        """Get a dog’s current daily goal and future daily goals.

        Set by an authorized user (if any).

        :param slug: uuid of the dog to look up
        :type slug: uuid
        :return: list of daily goals and dates set
        :rtype: json
        """
        r = self.get("/daily_goal/" + slug)
        r.raise_for_status()
        return r.json()

    def set_daily_goal(self, slug: str, data: Dict[str, Any]) -> Dict[str, str]:
        """Set the daily goal for a specified dog.

        Also get a response with future daily goals (if any). By default, a future
        daily goal is repeated for all future dates until another user-set goal is
        found. The daily goal can only be set for future dates, starting from the
        current date. The daily goal value needs to be a positive number.

        :param slug: uuid of the dog to modify
        :type slug: uuid
        :param data: dictionary containing two values, `daily_goal` and `date`
        :type data: dict
        :return: list of all future daily goals
        :rtype: json
        """
        r = self.put("/daily_goal/" + slug, json=data)
        r.raise_for_status()
        return r.json()

    # def _build_api_url(self, endpoint):
    #     return "{0}/v{1}/{endpoint}".format(
    #         self.API_ENDPOINT, self.API_VERSION, endpoint=endpoint)

    # def _get_common_args(self):
    #     return self.API_ENDPOINT, self.API_VERSION

    def _get_date_string(self, date: Optional[str]) -> Optional[str]:
        # if date is not None:
        #     date = parse(date)
        if not isinstance(date, str) and date is not None:
            return date.strftime("%Y-%m-%d")
        return date

    def get_activity_series(
        self,
        slug: str,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        resolution: Optional[str] = "DAILY",
    ) -> Dict[str, str]:
        """Get historical series data between two specified date times.

        The maximum range is 42 days with daily resolution, and 7 days with hourly
        resolution.

        :param slug: uuid of the dog to look up
        :type slug: uuid
        :param date_from: the start of the date range to look up
        :type date_from: datetime, date, str
        :param date_to: the end of the date range to look up
        :type date_to: datetime, date, str
        :param resolution: DAILY or HOURLY breakdown
        :type resolution: str
        :return: list of records breaking activity down
        :rtype: json
        """
        today = datetime.date.today()
        date_from = self._get_date_string(str(date_from))
        date_to = self._get_date_string(str(date_to))

        if date_from is None:
            date_from = (today - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

        if date_to is None:
            date_to = today.strftime("%Y-%m-%d")

        if resolution not in ["DAILY", "HOURLY"]:
            resolution = "DAILY"

        if date_to < date_from:
            raise ValueError("The to date must be after the from date")

        data = {
            "activity_series": {
                "slug": slug,
                "from": date_from,
                "to": date_to,
                "resolution": resolution,
            }
        }

        r = self.post("/activity_series", json=data)
        r.raise_for_status()
        return r.json()

    def get_dog_similar_stats(self, slug: str) -> Dict[str, str]:
        """Get this dogs, and similar dogs, statistics.

        :param slug: uuid of the dog to look up
        :type slug: uuid
        :return: statistics for dogs similar to the requested dog
        :rtype: json
        """
        r = self.post("/similar_dogs_stats", json={"slug": slug})
        r.raise_for_status()
        return r.json()

    def get_activity_totals(
        self, slug: str, date_from: Optional[str] = None, date_to: Optional[str] = None
    ) -> Dict[str, str]:
        """Get historical activity data by totaling the historical series.

        Between two specified date times.

        :param slug: uuid of the dog to look up
        :type slug: uuid
        :param date_from: the start of the date range to look up
        :type date_from: datetime, date, str
        :param date_to: the end of the date range to look up
        :type date_to: datetime, date, str
        :return: list of records breaking activity down
        :rtype: json
        """
        today = datetime.date.today()
        date_from = self._get_date_string(date_from)
        date_to = self._get_date_string(date_to)

        if date_from is None:
            date_from = (today - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

        if date_to is None:
            date_to = today.strftime("%Y-%m-%d")

        if date_to < date_from:
            raise ValueError("The to date must be after the from date")

        data = {"dog": {"slug": slug, "from": date_from, "to": date_to}}

        r = self.post("/activity_totals", json=data)
        r.raise_for_status()
        return r.json()

    def get_time_breakdown(
        self, slug: str, date_from: Optional[str] = None, date_to: Optional[str] = None
    ) -> Dict[str, str]:
        """Get the time (in minutes) spent at each activity level.

        For a certain dog between two specified date times.

        :param slug: uuid of the dog to look up
        :type slug: uuid
        :param date_from: the start of the date range to look up
        :type date_from: datetime, date, str
        :param date_to: the end of the date range to look up
        :type date_to: datetime, date, str
        :return: total minutes of each activity level (play, active, rest) for the
            period & dog
        :rtype: json
        """
        today = datetime.date.today()
        date_from = self._get_date_string(date_from)
        date_to = self._get_date_string(date_to)

        if date_from is None:
            date_from = (today - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

        if date_to is None:
            date_to = today.strftime("%Y-%m-%d")

        if date_to < date_from:
            raise ValueError("The to date must be after the from date")

        data = {"dog": {"slug": slug, "from": date_from, "to": date_to}}

        r = self.post("/time_breakdown", json=data)
        r.raise_for_status()
        return r.json()

    def get(self, path: str) -> Response:
        """Fetch a URL from the Fitbark API."""
        return self._request("get", path)

    def post(self, path: str, *, json: Dict[str, Any]) -> Response:
        """Post data to the Fitbark API."""
        return self._request("post", path, json=json)

    def put(self, path: str, *, json: Dict[str, Any]) -> Response:
        """Put data to the Fitbark API."""
        return self._request("put", path, json=json)

    def get_authorization_url(self, state: Optional[str] = None) -> Tuple[str, str]:
        """Get the authorization url."""
        return self._oauth.authorization_url(FITBARK_OAUTH, state)

    def request_token(
        self, authorization_response: Optional[str] = None, code: Optional[str] = None
    ) -> Dict[str, str]:
        """Fetch a Fitbark access token.

        :param authorization_response: Authorization response URL, the callback
                                       URL of the request back to you.
        :param code: Authorization code
        :return: A token dict
        """
        return self._oauth.fetch_token(
            FITBARK_TOKEN,
            authorization_response=authorization_response,
            code=code,
            client_secret=self.client_secret,
        )

    def refresh_tokens(self) -> Dict[str, Union[str, int]]:
        """Refresh and return new Fitbark tokens."""
        token = self._oauth.refresh_token(FITBARK_REFRESH)

        if self.token_updater is not None:
            self.token_updater(token)

        return token

    def _request(self, method: str, path: str, **kwargs: Any) -> Response:
        """Make a request.

        We don't use the built-in token refresh mechanism of OAuth2 session because
        we want to allow overriding the token refresh logic.
        """
        url = BASE_URL + path

        try:
            return getattr(self._oauth, method)(url, **kwargs)
        except TokenExpiredError:
            self._oauth.token = self.refresh_tokens()

            return getattr(self._oauth, method)(url, **kwargs)

    def hass_add_url(self) -> None:
        """Add callback url for auth."""
        if self._callback_url:
            callback_url = self._callback_url + "/auth/external/callback"
            access_token = self.hass_get_token()
            redirect_uri = self.hass_get_redirect_urls(access_token)
            if callback_url not in redirect_uri:
                redirect_uri = redirect_uri + "\r" + callback_url
                self.hass_add_redirect_urls(redirect_uri, access_token)
                _LOGGER.debug("Added %s redirect url", callback_url)

    def hass_remove_url(self) -> None:
        """Remove the callback url for auth."""
        if self._callback_url:
            callback_url = self._callback_url + "/auth/external/callback"
            access_token = self.hass_get_token()
            redirect_uri = self.hass_get_redirect_urls(access_token)
            if callback_url in redirect_uri:
                redirect_uri = redirect_uri.replace("\r" + callback_url, "")
                self.hass_add_redirect_urls(redirect_uri, access_token)
                _LOGGER.debug("Removed %s redirect url", callback_url)

    def hass_make_request(
        self, method: str, url: str, payload: Dict[str, str], headers: Dict[str, str]
    ) -> Dict[str, str]:
        """Wrap requests."""
        response = requests.request(method, url, json=payload, headers=headers)

        json_data = json.loads(response.text)
        # print(json_data)
        return json_data

    def hass_get_token(self) -> str:
        """Get the token."""
        url = "https://app.fitbark.com/oauth/token"
        payload = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": "fitbark_open_api_2745H78RVS",
        }
        headers = {"Content-Type": "application/json", "Cache-Control": "no-cache"}

        json_data = self.hass_make_request("POST", url, payload, headers)
        access_token = json_data["access_token"]
        return access_token

    def hass_get_redirect_urls(self, access_token: str) -> str:
        """Get a list of redirect URLs."""
        url = "https://app.fitbark.com/api/v2/redirect_urls"
        # payload = {}
        headers = {"Authorization": "Bearer " + access_token}
        json_data = self.hass_make_request("GET", url, {}, headers)
        redirect_uri = json_data["redirect_uri"]
        return redirect_uri

    def hass_add_redirect_urls(
        self, redirect_uri: str, access_token: str
    ) -> Dict[str, str]:
        """Add the redirect url."""
        url = "https://app.fitbark.com/api/v2/redirect_urls"
        payload = {"redirect_uri": redirect_uri}
        headers = {"Authorization": "Bearer " + access_token}
        json_data = self.hass_make_request("POST", url, payload, headers)
        return json_data
