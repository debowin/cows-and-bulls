"""
Contains the code for playing the cows & bulls game.

Q. how to use the wordlist - query db each time, linear search on list or dictionary lookup?
A. used dictionary lookup as linear search on list is naive and db queries involve I/O read delays.
"""

import random
from colorama import init, Fore, Style
import sqlite3

init()
sqlite_db = sqlite3.connect('words.db')

TURNS = 10  # attempts per word
HINTS = 7
REWARD_SCORE = 3
WORD_SIZE = 4  # 4, 5 or 6
KID_MODE = True
dictionary = {}
used = []


class Word(object):
    """
    the Word class contains all info about current word.
    """

    def __init__(self):
        self.name = ""
        self.meaning = ""
        self.cows = []
        self.bulls = []

    def get_arbitrary(self):
        """
        choose a random word from the word list
        """
        while True:
            randint = random.randint(0, len(dictionary.keys()) - 1)
            if randint not in used:
                break
        word = dictionary.keys()[randint]
        used.append(randint)
        self.name = word
        self.meaning = dictionary[word]
        self.cows = []
        self.bulls = []

    def try_guess(self, guess):
        """
        finds out the cows and bulls for a given guess.
        """
        self.cows = []
        self.bulls = []
        if guess == self.name:
            return True
        for i in range(WORD_SIZE):
            if guess[i] == self.name[i]:
                self.bulls.append(guess[i])
                continue
            try:
                self.name.index(guess[i])
                self.cows.append(guess[i])
            except ValueError:
                pass
        return False


def player_input(hints, hint_used):
    """
    Accept only a valid WORD_SIZE dictionary word as input.
    There shouldn't be any repeating characters.
    Accept ? for a hint only if hints are remaining.
    """
    while True:
        guess = raw_input('Guess(? for hint): ')
        if guess == '?' and hints > 0 and not hint_used:
            return '?'
        if len(guess) != WORD_SIZE:
            continue
        # perform dictionary check here.
        try:
            meaning = dictionary[guess.upper()]
            return guess.upper()
        except KeyError:
            continue


def kid_mode(guess, word):
    """
    Highlights letters according to cow or bull status.
    """
    for letter in guess:
        if letter in word.bulls:
            print Fore.RED + Style.BRIGHT + " " + letter,
        elif letter in word.cows:
            print Fore.GREEN + Style.BRIGHT + " " + letter,
        else:
            print Fore.RESET + Style.RESET_ALL + " " + letter,
    print Fore.RESET + Style.RESET_ALL


def print_status(word, guess, score, hints, hint_used):
    """
    prints the game status before each turn.
    """
    print "\nCOWS & BULLS"
    print "Hints:" + Fore.RED + Style.BRIGHT + ' ?' * hints + Fore.RESET + Style.RESET_ALL
    print "Score:" + Fore.YELLOW + Style.BRIGHT + ' $' * score + Fore.RESET + Style.RESET_ALL
    if hint_used:
        show_me_the_meaning(word, True)
    print "Cows: " + Fore.GREEN + "%d" % len(word.cows) + Fore.RESET + "\tBulls: " + Fore.RED + "%d" % len(
        word.bulls) + Fore.RESET
    if KID_MODE:
        kid_mode(guess, word)
    else:
        for letter in guess:
            print " " + letter


def get_words_from_db():
    """
    fetches words from db and adds them to word list.
    """
    global dictionary
    sql = "SELECT name, meaning FROM words WHERE LENGTH(name)=%d" % WORD_SIZE
    cursor = sqlite_db.execute(sql)
    for row in cursor.fetchall():
        dictionary[row[0]] = row[1]


def show_me_the_meaning(word, only_meaning):
    """
    Displays the word along with its meaning(s)
    """
    if not only_meaning:
        print "The word was:"
        print Fore.CYAN + Style.BRIGHT + "(+) %s" % word.name + Fore.RESET
    else:
        print "Meanings:"
    meanings = word.meaning.split('; ')
    for meaning in meanings:
        print Fore.YELLOW + Style.BRIGHT + "\t- %s" % meaning + Fore.RESET + Style.RESET_ALL


def main():
    """
    main function
    """
    get_words_from_db()
    score = 0
    hints = HINTS
    word = Word()
    while True:
        # Game Loop
        word.get_arbitrary()
        turn = 0
        hint_used = False
        guess = "____"
        while turn < TURNS:
            # Turn Loop
            print_status(word, guess, score, hints, hint_used)
            guess = player_input(hints, hint_used)
            if guess == '?':
                hint_used = True
                hints -= 1
                guess = "____"
                continue
            if word.try_guess(guess):
                score += 1
                print "BULL's Eye!"
                if score % REWARD_SCORE == 0 and hints < HINTS:
                    print "Congrats! You have been awarded a hint."
                    hints += 1
                break
            turn += 1
        else:
            print "Game Over."
            break
        show_me_the_meaning(word, False)
    raw_input('Press Enter')


if __name__ == "__main__":
    main()
