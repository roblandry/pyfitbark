# -*- coding: utf-8 -*-
"""Helper package for FitBark API."""
import logging
import os
import sys
import json

from argparse import ArgumentParser, Namespace

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
CALLBACK_URL = "http://192.168.1.10:8123"
# CALLBACK_URL = "http://domain.test.com"

# Setup Logging
_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s:[%(name)s][%(levelname)s]: %(message)s")
ch.setFormatter(formatter)
_LOGGER.addHandler(ch)


def argparser(args: List[str]) -> Namespace:
    """Construct the ArgumentParser for the CLI."""
    parser = ArgumentParser(prog="pyfitbark")
    # Redirect Logic
    parser.add_argument(
        "-g", "--get", help="Get redirect urls.", default=False, action="store_true"
    )
    parser.add_argument(
        "-r", "--reset", help="Reset redirect urls.", default=False, action="store_true"
    )
    parser.add_argument(
        "-a",
        "--add",
        help="Add CALLBACK redirect urls.",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "-x",
        "--remove",
        help="Remove CALLBACK redirect urls.",
        default=False,
        action="store_true",
    )
    # User data
    parser.add_argument(
        "-u", "--user", help="Get user profile.", default=False, action="store_true"
    )
    parser.add_argument(
        "--user-slug", help="Get user slug.", default=False, action="store_true"
    )
    parser.add_argument(
        "--user-pic", help="Get user picture.", default=False, action="store_true"
    )
    # Dog data
    parser.add_argument(
        "-d", "--dogs", help="Get user dogs.", default=False, action="store_true"
    )
    parser.add_argument(
        "--dog-slug", help="Get user dog slug(s).", default=False, action="store_true"
    )
    parser.add_argument(
        "--dog", help="Get dog info using slug.", default=False, action="store_true"
    )
    parser.add_argument(
        "--dog-pic",
        help="Get dog picture(s) using slug(s).",
        default=False,
        action="store_true",
    )
    return parser.parse_args(args)


class MainClass:
    """Main PyFitbark class."""

    def __init__(self) -> None:
        """Init."""
        self.client_id, self.client_secret = self.load_file()

        # mypy ERROR:
        # error: Argument "token_updater" to "FitbarkApi" has incompatible type
        # "Callable[[Dict[str, str]], None]"; expected "Optional[Callable[[str], None]]"
        self.api = FitbarkApi(
            self.client_id,
            self.client_secret,
            REDIRECT_URI,
            token=self.get_token(),
            token_updater=self.set_token,  # type: ignore
            callback_url=CALLBACK_URL,
        )

        self.do_auth()

    def load_file(self) -> Tuple[str, str]:
        """Load json from secrets file."""
        json_secrets = self.handle_secrets()
        client_id = json_secrets["client_id"]
        client_secret = json_secrets["client_secret"]
        if "INSERT IT HERE" in (client_id, client_secret):
            _LOGGER.critical("Please configure secrets.json!")
            sys.exit(1)
        else:
            return client_id, client_secret

    def handle_secrets(self) -> Dict[str, str]:
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
                    j_dict = json.loads(cache.read())
            except IOError:
                _LOGGER.critical("IO Error!")
                sys.exit(1)
            return j_dict

    def do_auth(self) -> None:
        """Load and verify secrets."""
        # Begin auth and load token
        if not os.path.isfile(TOKEN_FILE):
            authorization_url, _ = self.api.get_authorization_url()
            print("Please go to {} and authorize access.".format(authorization_url))
            authorization_response = input("Enter the Authorization Code: ")
            code = authorization_response
            self.set_token(self.api.request_token(code=code))

    def get_token(self) -> Dict[str, str]:
        """Get Token."""
        try:
            with open(TOKEN_FILE, "r") as cache:
                return json.loads(cache.read())
        except IOError:
            _LOGGER.critical("IO Error!")
            sys.exit(1)

    def set_token(self, token: Dict[str, str]) -> None:
        """Set Token."""
        with open(TOKEN_FILE, "w") as cache:
            cache.write(json.dumps(token))

    # COMMANDS
    def r_get(self) -> List[str]:
        """Get redirect urls."""
        token = self.api.hass_get_token()
        data = self.api.hass_get_redirect_urls(token)
        return data

    def r_reset(self) -> Dict[str, str]:
        """Reset redirect urls."""
        token = self.api.hass_get_token()
        data = self.api.hass_add_redirect_urls("urn:ietf:wg:oauth:2.0:oob", token)
        return data

    def r_add(self) -> List[str]:
        """Add CALLBACK_URL."""
        token = self.api.hass_get_token()
        self.api.hass_add_url()
        data = self.api.hass_get_redirect_urls(token)
        return data

    def r_remove(self) -> List[str]:
        """Remove CALLBACK_URL."""
        token = self.api.hass_get_token()
        self.api.hass_remove_url()
        data = self.api.hass_get_redirect_urls(token)
        return data

    def u_profile(self) -> Dict[str, str]:
        """Get various information about the specified user.

        This includes name, username (email address), profile picture and Facebook ID.
        """
        data = self.api.get_user_profile()
        return data

    def u_slug(self) -> str:
        """Get user slug."""
        profile = self.u_profile()
        data = profile["user"]["slug"]  # type: ignore
        return data

    def u_pic(self) -> str:
        """Get the Base64 encoded picture for a specified user."""
        user_slug = self.u_slug()
        user_pic = self.api.get_user_picture(user_slug)
        data = user_pic["image"]["data"]  # type: ignore
        return data

    def u_dogs(self) -> Dict[str, str]:
        """Get user dogs."""
        data = self.api.get_user_related_dogs()
        return data

    def u_dog_slug(self) -> List[str]:
        """Get dog slug(s)."""
        data = self.u_dogs()
        s_list = []
        # Loops all user dogs
        for dog in data["dog_relations"]:
            s_list.append(dog["dog"]["slug"])  # type: ignore
        return s_list

    def dog(self) -> List[Dict[str, Any]]:
        """Get various information about a certain dog.

        This includes name, breed, gender, weight, birthday and picture.
        """
        s_list = self.u_dog_slug()
        d_list = []
        # Loops all user dogs
        for dog in s_list:
            d_list.append(self.api.get_dog(dog))
        return d_list

    def d_pic(self) -> List[str]:
        """Get the Base64 encoded picture for a specified dog."""
        s_list = self.u_dog_slug()
        d_list = []
        # Loops all user dogs
        for dog in s_list:
            d = self.api.get_dog_picture(dog)
            s = d["image"]["data"]  # type: ignore
            d_list.append(s)
        return d_list


def main(opts: List[str]) -> None:
    """Main."""
    args = argparser(opts)

    api = MainClass()
    r: Any = None
    if args.get:
        r = api.r_get()
    elif args.reset:
        r = api.r_reset()
    elif args.add:
        r = api.r_add()
    elif args.remove:
        r = api.r_remove()

    elif args.user:
        r = api.u_profile()
    elif args.user_slug:
        r = api.u_slug()
    elif args.user_pic:
        r = api.u_pic()

    elif args.dogs:
        r = api.u_dogs()
    elif args.dog_slug:
        r = api.u_dog_slug()
    elif args.dog:
        r = api.dog()
    elif args.dog_pic:
        r = api.d_pic()

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

    if r:
        r = json.dumps(r, indent=2, separators=(",", ": "))
        print(r)


if __name__ == "__main__":
    main(sys.argv[1:])
