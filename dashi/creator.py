import genanki
import json
import yaml
import os
import random
import time
import logging
from genanki import Deck

from dashi.search import Kanji

CSS_STYLING = None  # To test if this works
if not os.path.isfile("./config.yml"):
    MODEL_NO = random.randrange(1 << 30, 1 << 31)
    DECK_NO = random.randrange(1 << 30, 1 << 31)
    with open("./config.yml", "w+") as stream:
        data = {"model_number": MODEL_NO, "deck_number": DECK_NO}
        yaml.safe_dump(data, stream)

else:
    with open("./config.yml", "r") as stream:
        data = yaml.safe_load(stream)
    MODEL_NO = data["model_number"]
    DECK_NO = data["deck_number"]

    if not data.get("css_styling"):
        CSS_STYLING = """      .card {
            font-family: mincho;
            font-size: 88px;
            text-align: center;
            color: black;
            }
            .kanji {font-family: "Kozuka Mincho Pr6N"}
            """
    else:
        CSS_STYLING = data.get("css_styling")
MODEL = genanki.Model(
    MODEL_NO,
    "Simple Model",
    fields=[
        {"name": "Kanji"},
        {"name": "Meaning"},
    ],
    templates=[
        {
            "name": "Card 1",
            "qfmt": '<span class="kanji">{{Kanji}}</span>',
            "afmt": "{{Meaning}}",
        }
    ],
    css=CSS_STYLING,
)


class MirinDeck(Deck):
    def __init__(
        self, deck_id=None, name=None, description="", jlpt_level=None, heisig=None
    ):
        super().__init__(deck_id=deck_id, name=name, description=description)
        self.jlpt_level = jlpt_level
        self.heisig = heisig

    def add_card_helper(self, data):
        """
        Args:
            Takes a dictionary of data. This is the request from kanjiapi.
        Returns:
            Nothing
        """
        kanji = data.get("kanji")
        meanings = ""
        on_readings = ""
        kun_readings = ""
        meanings = ", ".join(data["meanings"])
        on_readings = ", ".join(data["on_readings"])
        kun_readings = ", ".join(data["kun_readings"])
        time.sleep(2)  # Waiting 2 seconds is probably fine and permissable
        base = f"""
        on reading(s): {on_readings}
        kun readings: {kun_readings}
        meaning(s): {meanings}
        """
        logging.debug(f"Adding card for {kanji}...")
        if self.heisig and data.get("heisig_en"):
            # logging.info(data.get('heisig_en'))
            base += f"\nHeisig keyword: {data.get('heisig_en')}"
        # Uses the genanki note function and then uses the inherited add note method to add the note to the Deck.
        my_note = genanki.Note(model=MODEL, fields=[kanji, base])
        self.add_note(my_note)

    def _make(self, kanji_database, deck: Deck, jlpt, threshold):
        """
        Args:
            Takes a dictionary, deck, and parameters to make the deck based off.
            With this it will go through each of the databases and make a deck with it.

        """

        for kanji, frequency in kanji_database.items():
            if (jlpt is not None) and frequency >= threshold:
                r = Kanji.search_kanji(kanji).json()
                if (jlpt is not None and r.get("jlpt") is not None) and int(
                    r.get("jlpt")
                ) <= jlpt:
                    logging.info("JLPT level is within the treshold.")
                    # So in this case, the JLPT flag isn't None, and it is above the threshold and it's below the upper bound of JLPT.
                    deck.add_card_helper(r)
                    continue
                else:
                    logging.info("JLPT level is NOT within the treshold.")
                    continue
                # in this case the JLPT level is None, so just add as normal since it's above the treshold.
            elif frequency >= threshold:
                deck.add_card_helper(Kanji.search_kanji(kanji).json())

            else:
                # Doesn't qualify by any criteria
                continue

        return deck
