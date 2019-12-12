# /usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys

from language import translation


def check_for_double(path: str, filename: str) -> str:
    """
    Searches a directory for files with the desired filename.
    If a match is found a new filename will be created with a numbers system.
    Useful to prevent over-writing files.

    :param path: str Path to directory where the new file will be created.
    :param filename: str Filename to check for duplicates.

    :return: Returns an updated filename with an ascending number if duplicates found.
    :rtype: str
    """
    double_counter = 2
    temp_file_name = filename
    while os.path.exists(os.path.join(path, temp_file_name)):
        if len(filename.rsplit('.', 1)) > 1:
            temp_file_name = filename.rsplit('.', 1)[0] + \
                           '-' + str(double_counter) + '.' + \
                           filename.rsplit('.', 1)[1]
        else:
            temp_file_name += '-' + str(double_counter)
        double_counter += 1
    return temp_file_name


def is_yes_no(phrase):
    """
    # Ask as yes/no question and have the input check and turned into
    # a boolean. Compatible with all versions of Python.

    phrase: Yes/No phrase you would like to get input from user for

    returns: True for yes, False for no
    """
    # TODO: Remove language checking from here to better location
    while True:
        result = str(input(lang(phrase) + '[y/n] '))

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


def multi_choice(choices: tuple) -> int:
    """
    Prints the choices to console including a number for choosing.

    :param choices: tuple Strings for user to make a choice
    :return: Returns the index value for the choice
    :rtype: int
    """
    phrase = ''
    for i in range(len(choices)):
        phrase += choices[i] + '[' + str(i + 1) + '] '

    while True:
        result = int(input(phrase))

        if 0 <= result < len(choices):
            return result


def url_safe_string(text):
    for c in r'[]/\;,><&*:%=+@!#^()|?^':
        text = text.replace(c, '')
    return text
