# -*- coding: utf-8 -*-
"""Helper package for FitBark API."""
import logging
import os
import sys
import json

# pylint: disable=unused-import
from typing import Tuple, List, Optional, Union, Callable, Dict, Any  # NOQA

# pylint: disable=relative-beyond-top-level
from .api import FitbarkApi

# Test Accounts
# email: fake_001@fitbark.com
# email: fake_002@fitbark.com
# Password: 12345678

REDIRECT_URI = "urn:ietf:wg:oauth:2.0:oob"
TOKEN_FILE = "fitbark_auth.json"
SECRETS_FILE = "secrets.json"

# Setup Logging
_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s:[%(name)s][%(levelname)s]: %(message)s")
ch.setFormatter(formatter)
_LOGGER.addHandler(ch)


if __name__ == "__main__":

    def get_token() -> Dict[str, str]:
        """Get Token."""
        try:
            with open(TOKEN_FILE, "r") as cache:
                return json.loads(cache.read())
        except IOError:
            _LOGGER.critical("IO Error!")
            sys.exit(1)

    def set_token(token: Dict[str, str]) -> None:
        """Set Token."""
        with open(TOKEN_FILE, "w") as cache:
            cache.write(json.dumps(token))

    def handle_secrets() -> Dict[str, str]:
        """Create a secrets file if does not exist or load secrets."""
        if not os.path.isfile(SECRETS_FILE):
            data: Dict[str, str] = {
                "client_id": "INSERT IT HERE",
                "client_secret": "INSERT IT HERE",
            }
            with open(SECRETS_FILE, "w") as cache:
                cache.write(json.dumps(data))
            _LOGGER.critical("Secrets file created! Please configure secrets.json")
            sys.exit(1)
        else:
            try:
                with open(SECRETS_FILE, "r") as cache:
                    return json.loads(cache.read())
            except IOError:
                _LOGGER.critical("IO Error!")
                sys.exit(1)

    # Load and verify secrets
    json_secrets = handle_secrets()
    if json_secrets:
        client_id = json_secrets["client_id"]
        client_secret = json_secrets["client_secret"]
        if "INSERT IT HERE" in (client_id, client_secret):
            _LOGGER.critical("Please configure secrets.json!")
            sys.exit(1)

    # Setup API
    # mypy ERROR:
    # error: Argument "token_updater" to "FitbarkApi" has incompatible type
    # "Callable[[Dict[str, str]], None]"; expected "Optional[Callable[[str], None]]"
    api = FitbarkApi(
        client_id,
        client_secret,
        REDIRECT_URI,
        token=get_token(),
        token_updater=set_token,  # type: ignore
    )

    # Begin auth and load token
    if not os.path.isfile(TOKEN_FILE):
        authorization_url, _ = api.get_authorization_url()
        print("Please go to {} and authorize access.".format(authorization_url))
        authorization_response = input("Enter the Authorization Code: ")
        code = authorization_response
        set_token(api.request_token(code=code))

    # Get various information about the specified user including name,
    # username (email address), profile picture and Facebook ID.
    # r = api.get_user_profile()
    # _LOGGER.debug("\nProfile: \n%s\n", r)
    # # get user slug
    # user_slug = r["user"]["slug"]

    # # Get the Base64 encoded picture for a specified user.
    # r = api.get_user_picture(user_slug)
    # user_pic = r["image"]["data"]
    # _LOGGER.debug("\nUser Picture: \n%s\n", user_pic)

    # Get the dogs related to the user.
    # NECESSARY for follow on calls. Gets "dog_slug"
    r = api.get_user_related_dogs()
    # _LOGGER.debug("\nUser Dogs: \n%s\n", r)

    x = 0
    # mypy ERROR:
    # error: Item "None" of "Optional[str]" has no attribute "__iter__" (not iterable)
    for dog in r["dog_relations"]:  # type: ignore
        x += 1
        # mypy ERROR:
        # error: Item "str" of "Union[str, Any]" has no attribute "get"
        dog_slug: Dict[str, str] = dog["dog"]["slug"]  # type: ignore
        # _LOGGER.debug(dog_slug)

        # Get various information about a certain dog including name,
        # breed, gender, weight, birthday and picture.
        # response = api.get_dog(dog_slug)
        # _LOGGER.debug("\nDog %s: \n%s\n", x, response)

        # Get the Base64 encoded picture for a specified dog.
        # response = api.get_dog_picture(dog_slug)
        # _LOGGER.debug("\nDog %s Picture: \n%s\n", x, response)

        # Get a list of users currently associated with a specified dog,
        # together with the type of relationship (Owner or Friend) and privacy
        # settings for each user (how far back in time the activity data is visible).
        # response = api.get_dog_related_users(dog_slug)
        # _LOGGER.debug("\nDog %s Users: \n%s\n", x, response)

        # Get a dog’s current daily goal and future daily goals set by an authorized
        # user (if any).
        # response = api.get_daily_goal(dog_slug)
        # _LOGGER.debug("\nDog %s Daily Goal: \n%s\n", x, response)

        # Get historical series data between two specified date times.
        # date_from = "12/25/19"
        # response = api.get_activity_series(dog_slug, date_from=date_from)
        # _LOGGER.debug("\nDog %s Activity Series: \n%s\n", x, response)

        # Get this dogs, and similar dogs, statistics.
        # response = api.get_dog_similar_stats(dog_slug)
        # _LOGGER.debug("\nDog %s Simular Stats: \n%s\n", x, response)

        # Get historical activity data by totaling the historical series between two
        # specified date times.
        # date_from = "12/25/19"
        # response = api.get_activity_totals(dog_slug, date_from=date_from)
        # _LOGGER.debug("\nDog %s Activity Totals: \n%s\n", x, response)

        # Get the time (in minutes) spent at each activity level for a certain dog
        # between two specified date times.
        # date_from = "12/25/19"
        # response = api.get_time_breakdown(dog_slug, date_from=date_from)
        # _LOGGER.debug("\nDog %s Time Breakdown: \n%s\n", x, response)
