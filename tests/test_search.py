import pytest 
from dashi.search import Kanji
class TestSearch():
    def test_good_response(self): 
        kanji = "不"# we're going to test the search method with this
        assert Kanji.search_kanji(kanji).status_code == 200
    def test_bad_response(self):
        bad_string = "lksmdslaknfliakghhyla"
        assert Kanji.search_kanji(bad_string).status_code == 404
