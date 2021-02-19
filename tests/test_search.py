import unittest 
from dashi.search import Kanji
class TestSearch(unittest.TestCase):
    def test_good_response(self): 
        kanji = "不"# we're going to test the search method with this
        self.assertEqual(Kanji.search_kanji(kanji).status_code, 200)
    def test_bad_response(self):
        bad_string = "lksmdslaknfliakghhyla"
        self.assertEqual(Kanji.search_kanji(bad_string).status_code, 404)

if __name__ == "__main__":
    unittest.main()