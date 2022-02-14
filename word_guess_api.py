""" Word Guessing Microservice 
Pick a new word each day.
Compare guess word to hidden word. Is the word in the list?
For each letter give hints: 
(1) grey = not in word at all
(2) gold = in wrong spot
(3) green = in right spot
"""


import random
from datetime import date
from flask import Flask, jsonify, request
from words import getWordsList

app = Flask(__name__)


def getWord(wordsList):
    # get a random word from list
    number = random.randint(0, 844)
    dailyWord = wordsList[number]

    return dailyWord


def wordInList(guessWord):
    # return True if guess word in list, else False
    wordsList = getWordsList()
    if guessWord in wordsList:
        return True
    else:
        return False


def getHints(guessWord, dailyWord):
    # compare guess word to daily word
    # for each letter give hint: not-in, not-in-position, in-position
    secretLetters = list(dailyWord)
    guessLetters = list(guessWord)

    hints = dict(word=guessWord, letters=[
                                dict(letter=guessLetters[0], hint=''), 
                                dict(letter=guessLetters[1], hint=''), 
                                dict(letter=guessLetters[2], hint=''), 
                                dict(letter=guessLetters[3], hint=''), 
                                dict(letter=guessLetters[4], hint='')])

    for index, letter in enumerate(guessLetters):
        if letter not in secretLetters:
            hints['letters'][index]['hint'] = 'not-in'
        else:
            if letter == secretLetters[index]:
                hints['letters'][index]['hint'] = 'in-position'
            else:
                hints['letters'][index]['hint'] = 'not-in-position'

    return jsonify(hints)

# allows web app to make cross origin requests
@app.after_request
def cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

@app.route('/')
def get():
    """ api endpoint: url/?guess=GUESSWORD """

    guessWord = request.args.get('guess').upper()

    if not wordInList(guessWord):
        error = dict(error='Word not in list.')
        return jsonify(error)

    # pick a new word each day
    # current system date as string
    today = str(date.today())
    try:
        # read file for daily word
        with open('daily_word.txt', 'r') as file:
            content = file.readlines()
            dailyWord = content[0].strip()
            day = content[1]

            if day != today:
                # write new word and date to file
                with open('daily_word.txt', 'w') as file:
                    dailyWord = getWord(getWordsList())
                    file.write(dailyWord)
                    file.write('\n')
                    file.write(today)

    except:
        # write new word and date to file
        with open('daily_word.txt', 'w') as file:
            dailyWord = getWord(getWordsList())
            file.write(dailyWord)
            file.write('\n')
            file.write(today)

    finally:
        return getHints(guessWord, dailyWord)



if __name__ == '__main__':
    app.run(debug=True)