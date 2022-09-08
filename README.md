# :sake: mirin みりん :mount_fuji:

_Note:_ __This project uses the [genanki](https://github.com/kerrickstaley/genanki) and [KanjiAPI](https://github.com/onlyskin/kanjiapi.dev). It would not be much without these other projects, so please check them out.__

_mirin_ is a command line tool built with [Click](https://github.com/pallets/click) that aids the user in doing immersion study for the Japanese language by creating SRS Decks based on the kanji present in a given anime, movie, or drama. 

Specifically, it makes decks of SRS cards that will allow the user to learn some of the vocab and kanji used in the program that they are watching with or without subtitles.

*Note: I will be continually trying to improve this and make it more robust as far as useful stats to make your decks by, and other features*
## Usage

To create a deck based off _path-to-file.srt_, including only kanji that have been used 25 times or more,
```bash
    python mirin.py mirin --threshold 25 --file "./path-to-file.srt"
```
When prompted, enter the name of the deck for saving, and you're done!
*Note: for more info please check out the docs as well as running python mirin.py --help* 



## Features
- Decks made by _mirin_ are customizable!
  - They can be made via filtering Kanji by JLPT level, as well as usage stats.

| Command Argument  | Description                                                                                     | Required                      | 
|-------------------|-------------------------------------------------------------------------------------------------|-------------------------------|
| file STRING | The subtitle file you want to make an SRS deck of. [Default: None]  | :heavy_check_mark:   | 
| threshold INTEGER | Lower bound of usage threshold (how many times a kanji was used in the subtitle file) for a kanji to be included in the SRS deck.  [default: 100]      | :heavy_check_mark:   | 
| jlpt TEXT         | Only add kanji which are part of this JLPT level or lower. Case insensitive. I.e: N5, N4, N3... | :negative_squared_cross_mark: | 
| heisig BOOLEAN  | Specifies whether or not to include the Heisig keyword of this kanji.  | :negative_squared_cross_mark: |
```bash 
python mirin.py mirin --file "./path-to-file.srt" --threshold 90 --jlpt N2 
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
