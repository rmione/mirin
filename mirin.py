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

from dashi.search import Kanji
from dashi.creator import add_card, DECK_NO, MODEL
DATABASE_PATH = './databases'


def make_database(subtitle_array): 
    """
    Args:
        subtitle array: an array of subtitles(strings)
    Goes through each if the subtitles' strings character by character, checks if they are kanji, and
    if they are, adds them to the database.
    I can see this being really slow considering it's a double for loop
    
    Returns:
        sorted dictionary database of kanji
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
    print("brreh")
    """
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
def mirin(path, threshold, extract): 
    """ 
    this function is the main cli call. 


    """
    if extract: 
        extract_subs()
    

    for filename in os.listdir(path):
        # Individual deck level
        deck = genanki.Deck(DECK_NO, '')
        print(filename)
        
    
        with open(path+filename, 'r', encoding='utf-8') as file: 
            count = 0
            kanji_database = json.load(file)
            for kanji, frequency in kanji_database.items():
            
                
                if frequency >= threshold: 
                    r = Kanji.search_kanji(kanji)
                    
                    meanings = ', '.join(r["meanings"])
                    on_readings = ', '.join(r["on_readings"])
                    kun_readings = ', '.join(r["kun_readings"])
                    
                    time.sleep(2) # Waiting 2 seconds is probably fine and permissable
                    base = """
                    on reading(s): {0}
                    kun readings: {1}
                    meaning(s): {2}
                    """.format(on_readings, kun_readings, meanings)
                    print(base)
                    my_note = genanki.Note(
                        model=MODEL,
                        fields=[kanji, base])

                
                    deck.add_note(my_note)
                    
                else: 
                     continue 
        count +=1       
        if not os.path.isdir('./decks/'):
            os.mkdir('./decks/')
        genanki.Package(deck).write_to_file("./{0}{1}.apkg".format(filename, count))

    
if __name__ == "__main__":
    mirin()
    extract_subs()