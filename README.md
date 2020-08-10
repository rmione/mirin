# mirin みりん

This is a command line tool that aids the user in doing the Mass Immersion Approach for the Japanese language. Specifically, it makes decks of SRS cards that will allow the user to learn some of the vocab and kanji used in the program that they are watching without subtitles and in Japanese (legally, of course)

## To-dos:
### Basic Functionality
- Crawl subtitle database website and gets the subs for the desired show
- Either uses some API or Kanji dictionary to get the kanji. 
- Grabs the most commonly used readings of it 
- 
## More Advanced Functionality 
- Intelligent grabbing of Japanese words to get more complex verbs with kanji, i.e: 話します <- grab both the kanji　ご、はな etc and also the hiragana or other kanji after it, and make sense of the word that is there. This can come after the more basic functionality. 
- Ability to see combinations of kanji. 
- God this thing is actually going to have to be pretty smart to do this. Going to want to build it in Python in this case.. 