import requests
import json
import re

# -*- coding: utf-8 -*-

BASE_URL = "https://kanjiapi.dev/v1/kanji/"


class Kanji:
    @classmethod
    def search_kanji(cls, kanji):
        encoded = (BASE_URL + kanji).encode(
            "utf-8"
        )  # This looks like b'https://kanjiapi.dev/v1/kanji/\xe5\xa0\x82' etc
        decoded = encoded.decode("utf-8")
        # if response.status_code == 200:
        #     logging.info("Successful, status code {}".format(response.status_code))
        # else:
        #     logging.info("Unsuccessful error code {}".format(response.status_code))

        return requests.get(decoded)

    @classmethod
    def is_kanji(cls, kanji: str) -> bool:
        """
        Args:
            kanji: this is the unencoded "kanji" character.
        Returns:
            True if it is within the unicode range of kanji
            False if it is not.

        """

        if re.match("([一-龯])", kanji):
            return True
        return False
