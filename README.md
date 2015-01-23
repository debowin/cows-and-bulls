# COWS & BULLS
* word guessing game *
![Capture](https://raw.githubusercontent.com/debowin/cows-and-bulls/master/cap.jpg)
> The number of cows is the number of correctly guessed letters in incorrect positions.
> The number of bulls is the number of correctly guessed letters in the correct positions.
> In each turn, you get to enter a valid English word as a guess.
> Keep in mind, your word should have all unique letters and the word's length should be equal to the game's chosen word length.

## Features:
1. Can build the game DB by crawling a given word list.
2. Fetches word meanings from given word list or can harvest the results page of:
    * Merriam Webster Online
    * Longman Online
    dictionaries.
3. Has 8300+ pre-harvested english words + meanings in the game's SQLite DB where:
    * All letters in a word are unique.
    * Word sizes are either 4, 5 or 6.
4. Uses dictionary lookups to validate words that the user enters.
   (much more efficient than linear search on a list)
5. Uses the word meaning to provide hints at the cost of lives.
6. Reveals the word as well as its meaning at the end of a game,
   which is a nice way to increase your vocabulary.
7. Scoring system rewards the player with lives periodically.
8. Kid Mode - Highlights the cows and bulls with different colours.
9. Coloured CLI.

## Coming up:
* GUI support using Qt4