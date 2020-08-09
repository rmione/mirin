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
    for subtitle in os.listdir('./extracted/stuff'):
        print(subtitle)
        subs = pysrt.open('./extracted/stuff/'+subtitle, encoding='utf-8-sig')
        print(subs[0].text.encode('utf-8'))    
# extract_subs()
handle_srt()
print(sys.stdout.encoding)
