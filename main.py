import srt 
import os 
import zipfile
"""
This module will deal with searching the kanji and maybe making the cards
"""
print(os.listdir())
# with open(os.getcwd())
# for file in os.listdir():
#     print(file)
#     fn = str(file).split('.')[1]
#     print(fn[1])
#     if not fn[1] in ['zip', 'rar']:
#         continue 
#     # Otherwise it's a zipfile! 
#     with zipfile.ZipFile(os.getcwd() + file, 'r') as subtitle_archive: 
#         subtitle_archive.extractall("./extracted/{}".format(fn[0]))
fn = ["stuff"]
with zipfile.ZipFile('./stuff.zip', 'r') as subtitle_archive: 
    subtitle_archive.extractall("./extracted/{}".format(fn[0]))
        
