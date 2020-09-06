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
import logging
import pysubs2
import rarfile

from dashi.search import Kanji
from dashi.creator import Deck, DECK_NO, MODEL
if not os.path.isdir('./logs/'):
    os.mkdir('./logs/')

logger = logging.getLogger(__name__)
fh = logging.FileHandler('mirin.log')
fh.setLevel(logging.DEBUG)
fh.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
DATABASE_PATH = './databases/'
logger.info("Deck Number " + str(DECK_NO))

LOGO = """


           _      _       
 _ __ ___ (_)_ __(_)_ __  
| '_ ` _ \| | '__| | '_ \ 
| | | | | | | |  | | | | |
|_| |_| |_|_|_|  |_|_| |_|
                          


    """ 

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
    return {k: v for k, v in sorted(database.items(), key=lambda item: item[1])}

def handle_srt(path, threshold) -> tuple: 
    """
    Args: 
        None
    Returns:
        None
        This does most of the legwork. 
        Goes through the directory, 
        Then it goes through each of the individual subtitle file's contents. 
        It calls upon the make_database file and uses it to create databases for each "episode"
    """
    media_name = path.split('/')[-1]
    

    for subtitle in os.listdir(path):
        subs = pysubs2.load(path+'/'+subtitle, encoding='utf-8-sig')

        sorted_database = make_database(subs)
        current_db_path = "{0}/{1}/".format(DATABASE_PATH, subtitle)
        if not os.path.isdir(DATABASE_PATH):
            os.mkdir(DATABASE_PATH)
            os.mkdir(current_db_path)
        
        
        with open('./databases/{0}/{1}.json'.format(media_name, subtitle), 'w+', encoding='utf8') as f: 
            json.dump(sorted_database, f, ensure_ascii=False)
        # Database is sorted, here, so return a tuple of the highest use and the lowest use for this database. 
        return (list(sorted_database.values())[0], list(sorted_database.values())[-1])


@click.group() 
def mirin():
    pass 


@mirin.command('extract')
@click.option('--extract')
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
        if not fn[-1] in ['zip', 'rar']:
            continue 
    
        # Otherwise it's a zipfile! 
        if fn[-1] == 'zip':
             with zipfile.ZipFile('./{0}'.format(file), 'r') as subtitle_archive: 
                subtitle_archive.extractall("./extracted/{}".format(fn[0]))
        elif fn[-1] == 'rar':
            try: 
                with rarfile.RarFile('./{0}'.format(file), 'r') as subtitle_archive: 
                    subtitle_archive.extractall("./extracted/{}".format(fn[0]))
            except rarfile.RarCannotExec as e: 
                raise SystemExit("unrar or unar must be installed and in path to use rar files!")

@mirin.command('mirin')
@click.option('--threshold', type=int, default=100, show_default=True, help='Lower bound of usage threshold for a kanji to be included in the SRS deck.')
@click.option('--path', required=True, type=click.Path(exists=True), help='Path to the database for the desired media in this format: ./databases/media/')
@click.option('--jlpt', type=str, default=None, help='Only add kanji which are part of this JLPT level or lower. Case insensitive. I.e: N5, N4, N3...')
@click.option('--heisig', type=bool, default=None, help='Specify whether or not to include the RTK/Heisig keyword for this kanji if it exists.')
def handler(path, threshold, jlpt, heisig): 
    print(LOGO)
    """
    Args:
        path: database path
        threshold: lower bound on the usage thresholdfor a kanji to be included. 
        jlpt: string denoting the JLPT limit (inclusive)
    
    Click command arguments: 
    Options:
        --path PATH          Path to the database for the desired media in this
                            format: ./databases/media/  [required]

        --threshold INTEGER  Lower bound of usage threshold for a kanji to be
                            included in the SRS deck.  [default: 100]

        --jlpt TEXT          Only add kanji which are part of this JLPT level or
                            lower. Case insensitive. I.e: N5, N4, N3...

        --help               Show this message and exit.
    """
    # This makes all the needed databases.
    handle_srt(path, threshold)

    if jlpt is not None:
        if not re.search("^n[1-5]$", jlpt.lower()): 
            raise SystemExit("Improper input for --jlpt flag: {}".format(jlpt))
        jlpt = int(jlpt[1]) # grab the integer level
    
    
    decks = [] 
    if not os.path.isdir('./decks/'):
        os.mkdir('./decks/')
    for file in os.scandir('./databases/'):
        # Individual deck level
       
        deck = Deck(deck_id=DECK_NO, name=file.name, description='Deck generated by mirin', jlpt_level=jlpt, heisig=heisig)
        deck = deck._make(file, deck, jlpt, threshold) # Returns Deck object.
             
        
        decks.append(deck) # Appends to array of Deck objects.
    name = str(input("\033[1;31;40m Please enter the generic name of the deck(s): "))
    
    count = 0 
    for deck in decks: 
        deck.name = "{0}_Deck_{1}".format(name, count) # Makes a generic name based on the user input.
        genanki.Package(deck).write_to_file("./decks/{}.apkg".format(deck.name))
        count += 1 


    
if __name__ == "__main__":
    mirin()
    