import genanki 
import json 
import yaml 
import os
import random 

def load_config():
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


load_config()
with open('./testing_response.json', 'r') as stream: 
    data = json.load(stream)
    model = genanki.Model(
    1607392319,
    'Simple Model',
    fields=[
    {'name': 'Kanji'},
    {'name': 'Meaning'},
    ],
    templates=[
    {
        'name': 'Card 1',
        'qfmt': '<span class="kanji">{{Kanji}}</span>',
        'afmt': '{{Answer}}',
    } 
    ],
    css= """      .card {
                font-family: mincho;
                font-size: 88px;
                text-align: center;
                color: black;
               }
             .kanji {font-family: "Kozuka Mincho Pr6N"}
             """
    
    )
    my_note = genanki.Note(
        model=model,
        fields=[data["kanji"], 'Testing'])

    my_deck = genanki.Deck(
    2059400110,
    'Test Kanji')

    my_deck.add_note(my_note)
    genanki.Package(my_deck).write_to_file('testKanji.apkg')