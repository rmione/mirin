import genanki 
import json 
import yaml 
import os
import random 

# from dashi.search import Kanji
CSS_STYLING = 1929836198347019478 # To test if this works
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

    if data.get('css_styling'):
        CSS_STYLING = """      .card {
            font-family: mincho;
            font-size: 88px;
            text-align: center;
            color: black;
            }
            .kanji {font-family: "Kozuka Mincho Pr6N"}
            """
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




def add_card(deck, kanji, meaning):

    my_note = genanki.Note(
        model=model,
        fields=[kanji, meaning])

   
    deck.add_note(my_note)
def dump_deck(deck): 
    genanki.Package(deck).write_to_file('testKanji.apkg')