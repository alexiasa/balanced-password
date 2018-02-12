import os.path, math
import re
from re import match
import diceware
import random
import argparse
# from numpy import *
from diceware import *


keyboard = {
    "1": (-5, 2),
    "2": (-4, 2),
    "3": (-3, 2),
    "4": (-2, 2),
    "5": (-1, 2),
    "6": (1, 2),
    "7": (2, 2),
    "8": (3, 2),
    "9": (4, 2),
    "0": (5, 2),
    "q": (-5, 1),
    "w": (-4, 1),
    "e": (-3, 1),
    "r": (-2, 1),
    "t": (-1, 1),
    "y": (1, 1),
    "u": (2, 1),
    "i": (3, 1),
    "o": (4, 1),
    "p": (5, 1),
    "a": (-5, 0),
    "s": (-4, 0),
    "d": (-3, 0),
    "f": (-2, 0),
    "g": (-1, 0),
    "h": (1, 0),
    "j": (2, 0),
    "k": (3, 0),
    "l": (4, 0),
    "z": (-5, -1),
    "x": (-4, -1),
    "c": (-3, -1),
    "v": (-2, -1),
    "b": (-1, -1),
    "n": (1, -1),
    "m": (2, -1),
    " ": (0, 0),
    "-": (6, 2),
    ",": (3, -1),
    ".": (4, -1)
}


def get_diceware_pass(num_passwords):
    generated_passwords = []
    while len(generated_passwords) < num_passwords:
        diceware_pass = diceware.get_passphrase().lower()
        generated_passwords.append(diceware_pass)
    return "\n\n".join(generated_passwords)


def get_random_words(text, num_words=5):
    generated_words = []
    while len(generated_words) < num_words:
        choice = random.choice(text)
        generated_words.append(choice)
    return " ".join(generated_words)


def filter_length(input, min_length, max_length):
    return list([x for x in input if min_length <= len(x) <= max_length])


def get_scores(passphrase):
    initial_phrase_scores = []
    for word in passphrase:
        initial_phrase_scores.append(get_word_scores(word))
    return initial_phrase_scores


'''def get_word_scores(words):
    word_score = []
    for word in words:
        for letter in word:
            word_score.append(keyboard[letter])
    return sum(word_score)'''


def get_word_scores(words):
    word_score = []
    for word in words:
        for letter in word:
            word_score.append(sum(keyboard[letter]))
    return sum(word_score)


def calc_offset(scores):
    return sum(scores)


def get_options():
    """
    Get passphrase options from the user as input
    :return: the options as a list of strings to be passed to diceware's handle_options function
    """
    options = ['--no-caps']
    # default_options = ['--no-caps', '-n 4', '-d .']

    num_words_in_phrase = str(input("Select # of words in the passphrase. Please enter a number between 2 and 9.\n"))

    if not re.match("^[2-9]+", num_words_in_phrase):
        print("Not a valid selection. Using 4 words.")
        num_words_in_phrase = '4'

    num_words_in_phrase = '-n ' + num_words_in_phrase
    options.append(num_words_in_phrase)

    delimiter = str(input("Choose a delimiter ( - , . )\n"))

    if not re.match("[-,.]", delimiter):
        print("Not a valid selection. Using period as delimiter.")
        delimiter = '.'

    delimiter = '-d ' + delimiter

    options.append(delimiter)

    print("Passphrases will be printed in lowercase using your choice of delimiter between words.\n"
          "The resulting phrases scored as the most balanced over 3 sets of 100 generating and scoring iterations.")

    # ''.join(options)

    return options


if __name__ == '__main__':

    # dictionary = '/usr/share/dict/web2'
    # text = open(dictionary, 'r').read().lower().splitlines()
    # text = filter_length(text, 5, 7)

    diceware_opts = get_options()

    for i in range(1, 4):
        all_scores = []
        for x in range(1, 100):  # generate and score each passphrase

            word = diceware.get_passphrase(handle_options(diceware_opts))

            calculated_word_scores = get_scores(word)
            score = calc_offset(calculated_word_scores)
            all_scores.append((word, score))

        sorted_scores = sorted(all_scores, key=lambda x: abs(x[1]), reverse=True)

        balanced = sorted_scores[-4:]

        balanced_phrases = []
        for bal in balanced:
            balanced_phrases.append(bal[0] + "\n")

        print(" ".join(balanced_phrases))

# diceware.get_passphrase()

