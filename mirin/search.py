import requests
import json 
import re
# -*- coding: utf-8 -*-

BASE_URL = "https://kanjiapi.dev/v1/kanji/"
class Kanji: 
    @classmethod
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
    @classmethod
    def test_encoding(): 
        with open("./testing_response.json", 'r') as f:
            data = json.load(f)
            search_kanji(data['kanji'])
    @classmethod
    def is_kanji(kanji: str) -> bool: 
        """
        Args: 
            kanji: this is the unencoded "kanji" character. 
        Returns: 
            True if it is within the unicode range of kanji
            False if it is not. 

        """
        # regex = u"[\x3400-\x4DB5\x4E00-\x9FCB\xF900-\xFA6A]"

        print(str(kanji.encode('utf-8')))
        if re.match("([一-龯])", kanji):
            return True
        return False
# search_kanji("物")
# test_encoding()
print(is_kanji("s"))