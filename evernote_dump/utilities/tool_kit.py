# /usr/bin/env python3
# -*- coding: utf-8 -*-
import os


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


def make_dir_check(path: str) -> str:
    """
    # Check if path exists. If not found path is created
    # and the path is returned.

    :param path: str location of new directory

    :return: path
    :rtype: str
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


def path_safe_string(text: str) -> str:
    """
    Cleans the provided string for export to file system.

    :param text: string Text to be cleaned.

    :return: Cleaned string
    :rtype: str
    """
    for c in r'[]/\;,><&*:%=+@!#^()|?^':
        text = text.replace(c, '')

    clean = (("/", "／"), ("*", "＊"), (":", "："), ("¥", "￥"),
             ("?", "？"), ('"', "“"), ("<", "＜"), (">", "＞"), ("|", "-"))

    for a, b in clean:
        text = text.replace(a, b)

    return text
