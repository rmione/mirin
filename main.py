import srt 
import os 
import zipfile
import pysrt 
import sys
import re
import json
import operator

from mirin.search import Kanji

print(sys.getdefaultencoding())
def extract_subs(): 
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
    for subdir in os.listdir('./extracted/'):
        print(subdir)
        count = 0 
        for subtitle in os.listdir('./extracted/{}'.format(subdir)):
            subs = pysrt.open('./extracted/{0}/{1}'.format(subdir, subtitle), encoding='utf-8-sig')

            print("Subtitle " + subtitle)
            sorted_database = make_database(subs)

            with open('./{}.json'.format(subtitle), 'w+', encoding='utf8') as f: 
                json.dump(sorted_database, f, ensure_ascii=False)
            count += 1
extract_subs()
handle_srt()
print(sys.stdout.encoding)
