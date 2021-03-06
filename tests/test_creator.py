import pytest 
import yaml

from dashi.creator import MirinDeck
class TestCreator(): 
    """
    Test the methods in the creator module, not much to test but here goes.
    """


    def test_add_card(self):
        example_response = {
            "kanji": "蜜",
            "grade": 8,
            "stroke_count": 14,
            "meanings": [
                "honey",
                "nectar",
                "molasses"
            ],
            "kun_readings": [],
            "on_readings": [
                "ミツ",
                "ビツ"
            ],
            "name_readings": [],
            "jlpt": None,
            "unicode": "871c",
            "heisig_en": "honey"
            }
        test_deck = MirinDeck(name="New Test Deck")
        test_deck.add_card_helper(example_response)
        logging.info(str(test_deck.notes))
        assert len(test_deck.notes) >= 1
    def test_config_yml(self):
        # Assuming config yml exists...
        try:
            with open('./config.yml', 'r') as f: 
                data = yaml.safe_load(f)
                
                assert type(data) == dict
        except FileNotFoundError:
            SystemError("Somehow config.yml is not there, something has gone horribly wrong!")
    
    def test_dump_deck(self):
        # Create test deck to dump 
        test_deck = MirinDeck(name="New Test Deck")
    
