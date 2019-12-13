#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from xml.sax import make_parser, handler
from note_parser.note_parser import NoteParser
from utilities.settings import Settings


def run_parse(settings: Settings):
    """
    Start the parsing of an Evernote enex file.

    :args


    """
    # Setup xml parser
    parser = make_parser()
    parser.setFeature(handler.feature_namespaces, 0)

    for file in settings.files:
        base = os.path.basename(file)
        current_file = base.replace(".enex", "")
        note_handler = NoteParser(current_file, settings)
        parser.setContentHandler(note_handler)
        parser.parse(file)
