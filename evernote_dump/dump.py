#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from xml.sax import make_parser, handler
from note_parser.note_parser import NoteParser
from utilities.settings import Settings


def run_parse(settings: Settings, print_fun=None):
    """
    Start the parsing of an Evernote enex file.

    :param settings: Settings is a custom class to pass application wide settings.
    :param print_fun: func Pass in a callback function that will be passed a string for printing
                            and disable printing to console.
    """

    # Setup xml parser
    parser = make_parser()
    parser.setFeature(handler.feature_namespaces, 0)

    for file in settings.files:
        base = os.path.basename(file)
        current_file = base.replace(".enex", "")
        note_handler = NoteParser(current_file, settings, print_fun)
        parser.setContentHandler(note_handler)
        parser.parse(file)
