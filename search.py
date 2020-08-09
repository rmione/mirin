import requests
import json 
# -*- coding: utf-8 -*-

BASE_URL = "https://kanjiapi.dev/v1/kanji/"

def search_kanji(kanji):
    encoded = BASE_URL.encode('utf-8') # This looks like b'https://kanjiapi.dev/v1/kanji/\xe5\xa0\x82' etc
    print(encoded)
    decoded = encoded.decode('utf-8')
    response = requests.get(decoded)
    print(response.status_code)
    print(type(json.dumps(response.json())))
    with open("./testing_response.json", 'w+') as f:
        
        json.dump(response.json(), f)