import pysubs2
import json
import os
from dashi.search import Kanji
DATABASE_PATH = './databases/'

LOGO = """


           _      _       
 _ __ ___ (_)_ __(_)_ __  
| '_ ` _ \| | '__| | '_ \ 
| | | | | | | |  | | | | |
|_| |_| |_|_|_|  |_|_| |_|
                          


    """ 
class Misc:
    @staticmethod
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
    @staticmethod
    def handle_srt(path, threshold, num) -> tuple: 
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
        media_name = path.split('/')[-2]
        print("Medianame" + str(media_name))
        print(path)
        
        subs = pysubs2.load(path, encoding='utf-8-sig')

        sorted_database = Misc.make_database(subs)
        current_db_path = "{0}{1}/".format(DATABASE_PATH, media_name)
        
        try:
            # TODO: refactor this, maybe remove one or two of these, to cut the fat
            # os.mkdir('./databases/'+media_name)
            os.mkdir(DATABASE_PATH)
            os.mkdir(current_db_path)
        except FileExistsError: 
            pass
        
        with open('./databases/{0}/{1}.json'.format(media_name, num), 'w+', encoding='utf8') as f: 
            json.dump(sorted_database, f, ensure_ascii=False)
        # Database is sorted, here, so return a tuple of the highest use and the lowest use for this database. 
        return (list(sorted_database.values())[0], list(sorted_database.values())[-1])
