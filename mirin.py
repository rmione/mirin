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

from dashi.misc import Misc, LOGO
from dashi.creator import Deck, DECK_NO, MODEL

if not os.path.isdir('./logs/'):
    os.mkdir('./logs/')
console = logging.StreamHandler()
console.setLevel(logging.INFO)

logging.basicConfig(
    level=logging.INFO, 
    format='',
    handlers=[console]
    )

logging.debug("Deck Number " + str(DECK_NO))

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
        if not fn[-1] in ['zip']:
            continue 
    
        if fn[-1] == 'zip':
             with zipfile.ZipFile(f'./{file}', 'r') as subtitle_archive: 
                subtitle_archive.extractall(f"./extracted/{fn[0]}")
       

@mirin.command('mirin')
@click.option('--threshold', type=int, required=True, default=100, show_default=True, help='Lower bound of usage threshold for a kanji to be included in the SRS deck.')
@click.option('--jlpt', type=str, default=None, help='Only add kanji which are part of this JLPT level or lower. Case insensitive. I.e: N5, N4, N3...')
@click.option('--heisig', type=bool, default=None, help='Specify whether or not to include the RTK/Heisig keyword for this kanji if it exists.')
def handler(threshold, jlpt, heisig): 
    logging.info(f"Threshold: {str(threshold)} \nHeisig:{str(heisig)}")
    logging.info(LOGO)
    """
    Args:
        threshold: lower bound on the usage threshold for a kanji to be included. 
        jlpt: string denoting the JLPT limit (inclusive)
        heisig: boolean, specifiies whether or not to include the RTK/Heisig keyword for this kanji if it exists
    Click command arguments: 
    Options:
        --threshold INTEGER  Lower bound of usage threshold for a kanji to be
                            included in the SRS deck.  [default: 100]

        --jlpt TEXT          Only add kanji which are part of this JLPT level or
                            lower. Case insensitive. I.e: N5, N4, N3...

        --heisig BOOL         whether or not to include the RTK/Heisig keyword for this kanji if it exists
        --help               Show this message and exit.
    """    

    chosen_dir = Misc.choose_media()

    for i, file in enumerate(os.listdir(chosen_dir)):
        Misc.handle_srt(path=f'{chosen_dir}/{file}', threshold=threshold, num=i)
        
    if jlpt is not None:
        if not re.search("^n[1-5]$", jlpt.lower()): 
            raise SystemExit(f"Improper input for --jlpt flag: {jlpt}")
        jlpt = int(jlpt[1]) # grab the integer level
    
    decks = [] 
    if not os.path.isdir('./decks/'):
        os.mkdir('./decks/')
   
    for file in os.scandir('./databases/'):
        # Individual deck level
        for database in os.scandir(file):
            deck = Deck(deck_id=DECK_NO, name=file.name, description='Deck generated by mirin', jlpt_level=jlpt, heisig=heisig)
            deck = deck._make(database, deck, jlpt, threshold) # Returns Deck object.
                
            decks.append(deck) 

    name = str(input("\033[1;31;40m Please enter the generic name of the deck(s): "))
    logging.info(name)
    logging.info(f"Dumping {str(len(decks))}...")
    try:
        for count, deck in enumerate(decks): 
            deck.name = "{0}_Deck_{1}".format(name, count) # Makes a generic name based on the user input.
            genanki.Package(deck).write_to_file("./decks/{}.apkg".format(deck.name))
        logging.info("Decks successfully dumped! Exiting...")

    except Exception as e: 
        logging.error(str(e))

if __name__ == "__main__":
    mirin()