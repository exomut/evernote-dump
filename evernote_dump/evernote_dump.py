#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import xml

from .note_parser import NoteParser
from .tool_kit import is_yes_no, choose_language


def run_parse(args, path=""):
    # create an XMLReader
    parser = xml.sax.make_parser()

    # turn off namespaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    # override the default ContextHandler
    for i in range(0, len(args)):
        # pass in first argument as input file.
        if ".enex" in args[i]:
            base = os.path.basename(args[i])
            current_file = base.replace(".enex", "")
            handler = NoteParser(current_file, path)
            parser.setContentHandler(handler)
            parser.parse(args[i])


def main(args):

    # INIT Request user input
    choose_language()
    keep_file_names = is_yes_no('_keep_file_names_q')

    run_parse(args)
