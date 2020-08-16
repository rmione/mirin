# :sake: mirin みりん :mount_fuji:
__Note:__ __This project uses the [genanki](https://github.com/kerrickstaley/genanki) and [KanjiAPI](https://github.com/onlyskin/kanjiapi.dev). It would not be much without these other projects, so please check them out.__

_mirin_ is a command line tool that aids the user in doing the [Mass Immersion Approach for the Japanese language](https://massimmersionapproach.com/) by creating SRS Decks based on the kanji present in a given anime, movie, or drama. 

Specifically, it makes decks of SRS cards that will allow the user to learn some of the vocab and kanji used in the program that they are watching without subtitles and in Japanese.s

## Usage
 
1. Place the .srt archives of the show, anime, drama or movie that you want to make an SRS deck based off of into the root directory. 
2. 
```bash
    mirin.py --extract --path '/extracted/media_path/'--threshold 90
```

3. 

### To-dos: 
- add a flag for the N5-N1 kanji jlpt specification
  - Therefore I'll have to add more data to the databases when they are made. 
  - Also some more logic for dealing with this new data.
- 