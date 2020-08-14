import srt 
import os 
import zipfile
import pysrt 
import sys
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
        for subtitle in os.listdir('./extracted/{}'.format(subdir)):
            subs = pysrt.open('./extracted/{0}/{1}'.format(subdir, subtitle), encoding='utf-8-sig')
            print(str(subs[0].text.encode('utf-8')))
            with open('./testing.txt', 'w+') as f: 
                f.write(subs[0].text.decode('utf-8'))
extract_subs()
handle_srt()
print(sys.stdout.encoding)
