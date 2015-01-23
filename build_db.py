"""
contains the code to build the database of words from given source.
the provided sqlite file already contains most words
so you shouldn't have to use this.
the code must be changed according to the source of words.
functions have been provided for querying Merriam Webster and Longman online dictionaries
in case your word list doesn't have meanings as well.
"""

import csv
import sqlite3
import requests
from BSXPath import BSXPathEvaluator

csv_file = open('word_src/wordlist.txt', 'r')

csv_reader = csv.reader(csv_file)

sqlite_db = sqlite3.connect('words.db')


def exists_in_db(word):
    sql = "SELECT * FROM WORDS WHERE NAME='%s'" % word
    cursor = sqlite_db.execute(sql)
    if len(cursor.fetchall()) > 0:
        return True
    return False


def add_to_db(word, meaning):
    if exists_in_db(word):
        return
    # meaning = get_meaning_merweb(row[0].upper())
    meaning = get_meaning_longman(row[0].upper())
    if not meaning:
        return
    sql = 'INSERT INTO words(name, meaning) VALUES("%s", "%s")' % (word, meaning)
    sqlite_db.execute(sql)
    sqlite_db.commit()
    print "Added %s" % word


def get_meaning_merweb(word):
    url = 'http://www.merriam-webster.com/dictionary/%s' % word.lower()
    response = requests.get(url)
    if response.status_code != 200:
        return None
    source = response.text
    document = BSXPathEvaluator(source)
    print url
    definitions = document.getItemList("//div[@class='ld_on_collegiate']/p")
    if not definitions:
        return None
    definitions = [definition.text for definition in definitions]
    definition = "; ".join(definitions)
    # some filtering
    definition = definition.replace(': ', '')
    definition = definition.replace('lodash;', '')
    definition = definition.replace('&mdash;', '')
    print word, definition
    return definition


def get_meaning_longman(word):
    url = 'http://www.ldoceonline.com/search/?q=%s' % word.lower()
    print url
    response = requests.get(url)
    if response.status_code != 200:
        return None
    source = response.text
    document = BSXPathEvaluator(source)
    definitions = document.getItemList("//span[@class='DEF']")
    if not definitions:
        try:
            word_link = document.getFirstItem("//td[@class='hwdunSelMM']/a")['href']
            response = requests.get('http://www.ldoceonline.com'+word_link)
            source = response.text
            document = BSXPathEvaluator(source)
            definitions = document.getItemList("//span[@class='DEF']")
        except Exception, ex:
            print "Something went wrong.[%s]" % ex
            return None
    definitions = [definition.text for definition in definitions]
    definition = "; ".join(definitions)
    # some filtering
    definition = definition.replace('"', "'")
    print word, definition
    return definition

csv_reader.next()

for row in csv_reader:
    if not row:
        continue
    if not 7 > len(row[0]) > 3:  # EXCLUDE WORDS LARGER THAN 6 CHARS
        continue
    if len(row[0]) == len(set(row[0])):  # EXCLUDE REPEATED LETTER WORDS
        # add_to_db(row[0].upper(), row[1].lower())
        add_to_db(row[0].upper(), '')