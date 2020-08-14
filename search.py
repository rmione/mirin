import requests
import json 
# -*- coding: utf-8 -*-

BASE_URL = "https://kanjiapi.dev/v1/kanji/"

def search_kanji(kanji):
    print(kanji)
    encoded = (BASE_URL+kanji).encode('utf-8') # This looks like b'https://kanjiapi.dev/v1/kanji/\xe5\xa0\x82' etc
    print(encoded)
    decoded = encoded.decode('utf-8')
    response = requests.get(decoded)
    if response.status_code == 200: 
        print("Successful, status code {}".format(response.status_code))
    else: 
        print("Unsuccessful error code {}".format(response.status_code))
    
    with open("./testing_response.json", 'w+') as f:
        json.dump(response.json(), f)

def test_encoding(): 
    with open("./testing_response.json", 'r') as f:
        data = json.load(f)
        search_kanji(data['kanji'])


# search_kanji("物")
test_encoding()