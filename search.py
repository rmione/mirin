import requests
import json 
# -*- coding: utf-8 -*-

base_url = "https://kanjiapi.dev/v1/kanji/堂"
kanji = "堂"

encoded = base_url.encode('utf-8')
decoded = encoded.decode('utf-8')
response = requests.get(decoded)
print(response.status_code)
with open("./testing_response.json", 'w+') as f:
    json.dump(response.json(), f)