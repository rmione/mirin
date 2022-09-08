import pysubs2
import json
import os
import logging
from dashi.search import Kanji

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
                    database[char] += 1
        return {k: v for k, v in sorted(database.items(), key=lambda item: item[1])}

    @staticmethod
    def handle_srt(path, threshold, num) -> tuple:
        """
        Args:
            None
        Returns:
            None
            This does most of the legwork.
            Then it goes through the individual subtitle file's contents.
            It calls upon the make_database file and uses it to create databases for each "episode"
        """
        media_name = path
        subs = pysubs2.load(path, encoding="utf-8-sig")
        logging.info(f"Current media name: {media_name}")
        sorted_database = Misc.make_database(subs)

        # Return the sorted dictionary
        return sorted_database
