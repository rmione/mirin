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

from dashi.misc import Misc, LOGO
from dashi.creator import Deck, DECK_NO, MODEL

if not os.path.isdir('./logs/'):
    os.mkdir('./logs/')

logger = logging.getLogger(__name__)
fh = logging.FileHandler('mirin.log')
fh.setLevel(logging.DEBUG)
fh.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
logger.info("Deck Number " + str(DECK_NO))



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

def choose_media():
        files = list(os.scandir('./extracted/'))
        for file in list(files):
            print(file.name)
            if input("Is this the media subs you want to make a deck of? (y/n): ").lower().strip()[:1] == "y": return file.path
            else: pass

            if files.index(file) == len(files)-1:
                raise SystemExit
@mirin.command('mirin')
@click.option('--threshold', type=int, default=100, show_default=True, help='Lower bound of usage threshold for a kanji to be included in the SRS deck.')
@click.option('--path', required=True, type=click.Path(exists=True), help='Path to the database for the desired media in this format: ./databases/media/')
@click.option('--jlpt', type=str, default=None, help='Only add kanji which are part of this JLPT level or lower. Case insensitive. I.e: N5, N4, N3...')
@click.option('--heisig', type=bool, default=None, help='Specify whether or not to include the RTK/Heisig keyword for this kanji if it exists.')
def handler(path, threshold, jlpt, heisig): 
    logging.info(f"Path: {str(path)} \nThreshold: {str(threshold)} \nHeisig:{str(heisig)}")
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
    
    chosen_dir = choose_media()
    print("ypoo")
    print(chosen_dir)
    i = 0
    for file in os.listdir(chosen_dir):
        Misc.handle_srt(path='{0}/{1}'.format(chosen_dir, file), threshold=threshold, num=i)
        i = i + 1
    if jlpt is not None:
        if not re.search("^n[1-5]$", jlpt.lower()): 
            raise SystemExit("Improper input for --jlpt flag: {}".format(jlpt))
        jlpt = int(jlpt[1]) # grab the integer level
    
    
    decks = [] 
    if not os.path.isdir('./decks/'):
        os.mkdir('./decks/')
   
    for file in os.scandir('./databases/Absolute Duo (01-12)'):
        # Individual deck level
        print("FILEEE")
        print(file)
        deck = Deck(deck_id=DECK_NO, name=file.name, description='Deck generated by mirin', jlpt_level=jlpt, heisig=heisig)
        deck = deck._make(file, deck, jlpt, threshold) # Returns Deck object.
             
        
        decks.append(deck) # Appends to array of Deck objects.
    name = str(input("\033[1;31;40m Please enter the generic name of the deck(s): "))
    logger.info(name)
    count = 0 
    print("Length of decks array : " +str(len(decks)))
    for deck in decks: 
        deck.name = "{0}_Deck_{1}".format(name, count) # Makes a generic name based on the user input.
        genanki.Package(deck).write_to_file("./decks/{}.apkg".format(deck.name))
        count += 1 


    
if __name__ == "__main__":
    mirin()
    