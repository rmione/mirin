import srt 
import os 
import zipfile
import pysrt 
import sys
import re
import json
import operator
from mirin.search import Kanji
"""
This module will deal with searching the kanji and maybe making the cards
"""
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
def handle_srt(): 
    """
    This function is tentative.
    For not it opens the subtitle files and writes the first sub to a file. I'm just testing encoding and stuff with this, 
    """
    for subdir in os.listdir('./extracted/'):
        print(subdir)
        count = 0 
        for subtitle in os.listdir('./extracted/{}'.format(subdir)):
            subs = pysrt.open('./extracted/{0}/{1}'.format(subdir, subtitle), encoding='utf-8-sig')
            # print(str(subs[0].text.encode('utf-8')))
            # with open('./testing.txt', 'w+') as f: 
            #     f.write(subs[0].text.decode('utf-8'))
            print("Subtitle " + subtitle)
           
            database = {}

            # This is subtitle level
            for sub in subs: 
                arr = sub.text
                # This is the sentence level
                for char in arr:
                    if Kanji.is_kanji(char):
                        if not database.get(char):
                            # Initialize database entry and zero count 
                            database[char] = 0
                        database[char]+=1
                        # count +=1 
            x = {k: v for k, v in sorted(database.items(), key=lambda item: item[1])}
            with open('./kanji{}.json'.format(count), 'w+', encoding='utf8') as f: 
                json.dump(x, f, ensure_ascii=False)
            count += 1
            # print(database)
extract_subs()
handle_srt()
print(sys.stdout.encoding)
