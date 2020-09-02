import genanki 
import json 
import yaml 
import os
import random 
import time
from genanki import Deck
# from dashi.search import Kanji
CSS_STYLING = None # To test if this works
if not os.path.isfile('./config.yml'): 
    MODEL_NO = random.randrange(1 << 30, 1 << 31)
    DECK_NO = random.randrange(1 << 30, 1 << 31)
    with open('./config.yml', 'w+') as stream: 
        data = {
            "model_number": MODEL_NO,
            "deck_number": DECK_NO
        }
        yaml.safe_dump(data, stream)
        
else: 
    with open('./config.yml', 'r') as stream:
        data = yaml.safe_load(stream)
    MODEL_NO = data["model_number"]
    DECK_NO = data["deck_number"]

    if not data.get('css_styling'):
        CSS_STYLING = """      .card {
            font-family: mincho;
            font-size: 88px;
            text-align: center;
            color: black;
            }
            .kanji {font-family: "Kozuka Mincho Pr6N"}
            """
    else: 
        CSS_STYLING = data.get('css_styling')
MODEL = genanki.Model(
MODEL_NO,
'Simple Model',
fields=[
{'name': 'Kanji'},
{'name': 'Meaning'},
],
templates=[
{
    'name': 'Card 1',
    'qfmt': '<span class="kanji">{{Kanji}}</span>',
    'afmt': '{{Meaning}}',
} 
],
css=CSS_STYLING

)


class Deck(Deck):
    def __init__(self, deck_id=None, name=None, description='', jlpt_level=None, heisig=None): 
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
        kanji = data.get('kanji')
        meanings = ""
        on_readings = ""
        kun_readings = ""
        meanings = ', '.join(data["meanings"])
        on_readings = ', '.join(data["on_readings"])
        kun_readings = ', '.join(data["kun_readings"])
        
        time.sleep(2) # Waiting 2 seconds is probably fine and permissable
        base = """
        on reading(s): {0}
        kun readings: {1}
        meaning(s): {2}
        """.format(on_readings, kun_readings, meanings)
        if self.heisig and data.get('heisig_en'):
            # print(data.get('heisig_en'))
            base += "\nHeisig keyword: {}".format(data.get('heisig_en'))
        # Uses the genanki note function and then uses the inherited add note method to add the note to the Deck.
        my_note = genanki.Note(
            model=MODEL,
            fields=[kanji, base])
        self.add_note(my_note)
