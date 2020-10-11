# :sake: mirin みりん :mount_fuji:

_Note:_ __This project uses the [genanki](https://github.com/kerrickstaley/genanki) and [KanjiAPI](https://github.com/onlyskin/kanjiapi.dev). It would not be much without these other projects, so please check them out.__

_mirin_ is a command line tool built with [Click](https://github.com/pallets/click) that aids the user in doing the [Mass Immersion Approach for the Japanese language](https://massimmersionapproach.com/) by creating SRS Decks based on the kanji present in a given anime, movie, or drama. 

Specifically, it makes decks of SRS cards that will allow the user to learn some of the vocab and kanji used in the program that they are watching without subtitles and in Japanese.

*Note: I will be continually trying to improve this and make it more robust as far as useful stats to make your decks by, and other features*
## Usage
 
1. Place the compressed subtitle archives of the show, anime, drama or movie that you want to make an SRS deck based off of into the root directory. 
2. In your terminal of choice run the following example commands: 
```bash
    python mirin.py extract
    python mirin.py mirin --threshold 90
```
*Note: for more info please check out the docs as well as running python mirin.py --help* 

*Note: to use .rar archives for your subtitles automatically, please install unrar and have it on your PATH.*

3. In the terminal window, the program will prompt ask you what subfolder to /extracted/ you want to make decks of. 
4. When prompted, input "y" when it shows the desired media subfolder in /extracted/. 
5. Wait for the process to be complete.
6. Navigate to the /decks/ directory and see your SRS decks made to your specification.

## Features
- Decks made by _mirin_ are customizable!
  - They can be made via filtering Kanji by JLPT level, as well as usage stats.

| Command Argument  | Description                                                                                     | Required                      |   |   |
|-------------------|-------------------------------------------------------------------------------------------------|-------------------------------|---|---|
| threshold INTEGER | Lower bound of usage threshold for a kanji to be included in the SRS deck.  [default: 100]      | :heavy_check_mark:   |   |   |
| jlpt TEXT         | Only add kanji which are part of this JLPT level or lower. Case insensitive. I.e: N5, N4, N3... | :negative_squared_cross_mark: |   |   |
```bash 
python mirin.py mirin --threshold 90 --jlpt N2
```
- You can specify your card's CSS styling in the config.yml file. You *must* use a multi-line string. 
  For example, 

```yaml
css_styling: > 
            .card {
            font-family: mincho;
            font-size: 88px;
            text-align: center;
            color: black;
            }
            .kanji {font-family: "Kozuka Mincho Pr6N"}
```
