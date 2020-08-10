import genanki 
import json 

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