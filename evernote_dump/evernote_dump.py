#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
from xml.sax import make_parser, handler

from tool_kit import is_yes_no, choose_language
from note_parser import NoteParser


def run_parse(args, path=""):
    """
    Start the parsing of an Evernote enex file.

    :args


    """
    # Setup xml parser
    parser = make_parser()
    parser.setFeature(handler.feature_namespaces, 0)

    for i in range(0, len(args)):
        # pass in first argument as input file.
        if ".enex" in args[i]:
            base = os.path.basename(args[i])
            current_file = base.replace(".enex", "")
            note_handler = NoteParser(current_file, path)
            parser.setContentHandler(note_handler)
            parser.parse(args[i])


def run_cli_ui(args, path=''):

    choose_language()
    keep_file_names = is_yes_no('_keep_file_names_q')

    run_parse(args)


if __name__ == "__main__":

    run_cli_ui(sys.argv[1:])
