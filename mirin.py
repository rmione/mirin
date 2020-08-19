import srt 
import os 
import zipfile
import pysrt 
import sys
import re
import json
import operator
import click
import genanki 
import time
from genanki.deck import Deck
from dashi.search import Kanji
from dashi.creator import add_card, DECK_NO, MODEL
DATABASE_PATH = './databases'
print("Deckno " + str(DECK_NO))
class Deck(Deck):
    def __init__(self, deck_id=None, name=None, description='', jlpt_level=None): 
        super().__init__(deck_id=deck_id, name=name, description=description)
        self.jlpt_level = jlpt_level
    def add_card_helper(self, data): 
        kanji = data.get('kanji')
        meanings = ""
        on_readings = ""
        kun_readings = ""
        meanings = ', '.join(data["meanings"])
        on_readings = ', '.join(data["on_readings"])
        kun_readings = ', '.join(data["kun_readings"])
        
        time.sleep(2) # Waiting 2 seconds is probably fine and permissable
        base = """
        on reading(s): {0}
        kun readings: {1}
        meaning(s): {2}
        """.format(on_readings, kun_readings, meanings)
        
        my_note = genanki.Note(
            model=MODEL,
            fields=[kanji, base])


        self.add_note(my_note)

def make_database(subtitle_array): 
    """
    Args:
        subtitle array: an array of subtitles(strings)
    
    
    Returns:
        sorted dictionary database of kanji
        Goes through each if the subtitles' strings character by character, checks if they are kanji, and
        if they are, adds them to the database.
        I can see this being really slow considering it's a double for loop
    """
    database = {}
    # This is subtitle level
    for sub in subtitle_array: 
        # This is the sentence level
        for char in sub.text:
            if Kanji.is_kanji(char):
                if not database.get(char):
                    # Initialize database entry and zero count 
                    database[char] = 0
                database[char]+=1
                # count +=1 
    return {k: v for k, v in sorted(database.items(), key=lambda item: item[1])}

def handle_srt(): 
    """
    Args: 
        None
    Returns:
        None
        This does most of the legwork. 
        Goes through the /extracted/ directory, and finds the media's subfolder.
        Then it goes through each of the individual subtitle file's contents. 
        It calls upon the make_database file and uses it to create databases for each "episode"
    """
    for subtitle_directory in os.listdir('./extracted/'):
        print(subtitle_directory)
        count = 0 
        for subtitle in os.listdir('./extracted/{}'.format(subtitle_directory)):
            subs = pysrt.open('./extracted/{0}/{1}'.format(subtitle_directory, subtitle), encoding='utf-8-sig')

            sorted_database = make_database(subs)
            current_db_path = "{0}/{1}/".format(DATABASE_PATH, subtitle_directory)
            if not os.path.isdir(current_db_path):
                os.mkdir(DATABASE_PATH)
                os.mkdir(current_db_path)
            with open(current_db_path + "{}.json".format(subtitle), 'w+', encoding='utf8') as f: 
                json.dump(sorted_database, f, ensure_ascii=False)
            count += 1


def extract_subs(extract): 
    
    """
    Args: 
        None
    Returns: 
        None
        Goes through the root directory, and does some logic to figure out whether or not something is subtitle archive.
        If it is, it extracts it to its own subdirectory within the /extracted/ directory.
    """
    for file in os.listdir(): 
        if not os.path.isfile(file): 
            continue 

        fn = file.split('.')
        if not fn[1] in ['zip', 'rar']:
            continue 
    
        # Otherwise it's a zipfile! 
        with zipfile.ZipFile('./{0}'.format(file), 'r') as subtitle_archive: 
            subtitle_archive.extractall("./extracted/{}".format(fn[0]))


@click.group(invoke_without_command=True)
@click.option('--path', required=True, type=click.Path(exists=True), help='Path to the database for the desired media in this format: ./databases/media/')
@click.option('--threshold', type=int, default=100, show_default=True, help='Lower bound of usage threshold for a kanji to be included in the SRS deck.')
@click.option('--extract', type=bool, default=False, show_default=True, help='If True, all zip files in the root directory will be extracted into the /extracted/ directory. Set it to True for the first time.')
@click.option('--jlpt', type=str, default=None, help='Only add kanji which are part of this JLPT level or lower. Case insensitive. I.e: N5, N4, N3...')
def mirin(path, threshold, extract, jlpt): 
    """ 
    this function is the main cli call. 
    Args:
        path: database path
        threshold: lower bound on the usage thresholdfor a kanji to be included. 
        extract: boolean flag 
        jlpt: string denoting the JLPT limit (inclusive)
    Click command arguments: 
    Options:
        --path PATH          Path to the database for the desired media in this
                            format: ./databases/media/  [required]

        --threshold INTEGER  Lower bound of usage threshold for a kanji to be
                            included in the SRS deck.  [default: 100]

        --extract BOOLEAN    If True, all zip files in the root directory will be
                            extracted into the /extracted/ directory. Set it to
                            True for the first time.  [default: False]

        --jlpt TEXT          Only add kanji which are part of this JLPT level or
                            lower. Case insensitive. I.e: N5, N4, N3...

        --help               Show this message and exit.
    """
    if jlpt is not None:
        
        if not re.search("^n[1-5]$", jlpt.lower()): 
            raise SystemExit("Improper input for --jlpt flag: {}".format(jlpt))
        jlpt = int(jlpt[1]) # grab the integer level
    if extract: 
        extract_subs()
    
    for filename in os.listdir(path):
        # Individual deck level
        deck = Deck(deck_id=DECK_NO, name=filename, description='Deck generated by mirin', jlpt_level=jlpt)
        print("Jlpt level: " + str(deck.jlpt_level))
        print(filename)
        
        print(jlpt)
        with open(path+filename, 'r', encoding='utf-8') as file: 
            count = 0
            kanji_database = json.load(file)
            for kanji, frequency in kanji_database.items():
                if (jlpt is not None) and frequency >= threshold: 
                    
                    r = Kanji.search_kanji(kanji)
                    if int(r.get('jlpt')) <= jlpt:
                        print("jlpt level passes")
                    # So in this case, the JLPT flag isn't None, and it is above the threshold and it's below the upper bound of JLPT.
                        deck.add_card_helper(Kanji.search_kanji(kanji))
                        continue
                    else: 
                        print("jlpt level doesnt pass")
                        continue

                    # in this case the JLPT level is None, so just add as normal since it's above the treshold.
                elif frequency >= threshold:
        
                    deck.add_card_helper(Kanji.search_kanji(kanji))
                else: 
                    # Doesn't qualify by any criteria
                     continue 
        count +=1       
        if not os.path.isdir('./decks/'):
            os.mkdir('./decks/')
        genanki.Package(deck).write_to_file("./decks/{0}_Deck{1}.apkg".format(filename, count))

    
if __name__ == "__main__":
    mirin()
    extract_subs()