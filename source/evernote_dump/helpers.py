# /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from .language import translation


def check_for_double(path, filename):
    """
    # Make sure the path has a trailing /
    # Check file path and modifies it if a duplicate is found.
    # Used for creating new files.
    # Works with file extensions too.

    path: to desired save point

    returns: an updated path if path double found
    """
    doubleCounter = 2
    tempFileName = filename
    while os.path.exists(os.path.join(path, tempFileName)):
        if len(filename.rsplit('.', 1)) > 1:
            tempFileName = filename.rsplit('.', 1)[0] + \
                           '-' + str(doubleCounter) + '.' + \
                           filename.rsplit('.', 1)[1]
        else:
            tempFileName += '-' + str(doubleCounter)
        doubleCounter += 1
    return tempFileName


def is_python_three():
    if sys.version_info[:2] <= (2, 7):
        return False
    else:
        return True


def is_yes_no(phrase):
    """
    # Ask as yes/no question and have the input check and turned into
    # a boolean. Compatible with all versions of Python.

    phrase: Yes/No phrase you would like to get input from user for

    returns: True for yes, False for no
    """
    while True:
        if is_python_three():
            result = str(input(lang(phrase) + '[y/n] '))
        else:
            result = str(raw_input(lang(phrase) + '[y/n] '))

        if result.lower() == 'yes' or result.lower() == 'y':
            return True
        elif result.lower() == 'no' or result.lower() == 'n':
            return False
        print(lang('_y_or_n_please'))


def lang(phrase):
    try:
        if phrase in translation[selang]:
            return translation[selang][phrase]
        else:
            return phrase + " (NEEDS TRANSLATION)"
    except (UnboundLocalError, NameError):
        return translation['English'][phrase]


def choose_language():
    global selang
    phrase = ''
    counter = 1
    languages = []
    for language in sorted(translation.keys()):
        phrase += '[' + str(counter) + ']' + language + ' '
        languages.append(language)
        counter += 1

    while True:
        if sys.version_info[:2] <= (2, 7):
            try:
                result = int(raw_input(phrase))
            except Exception:
                result = -1
        else:
            try:
                result = int(input(phrase))
            except Exception:
                result = -1

        if len(languages) >= result > 0:
            selang = languages[result - 1]
            break


def make_dir_check(path):
    """
    # Check if path exists. If not found path is created
    # and the path is returned.

    path: location of new directory

    returns: path
    """
    if not os.path.exists(path):
        os.makedirs(path)

    return path


def multi_choice(inTuple):
    """
    # Input a Tuple of choices.
    # Returns the user's choice as tuple entry
    """
    phrase = ''
    for i in range(len(inTuple)):
        phrase += inTuple[i] + '[' + str(i + 1) + '] '

    while True:
        if sys.version_info[:2] <= (2, 7):
            result = int(raw_input(phrase))
        else:
            result = int(input(phrase))

        if 0 <= result < len(inTuple):
            return result


def url_safe_string(text):
    for c in r'[]/\;,><&*:%=+@!#^()|?^':
        text = text.replace(c, '')
    return text
