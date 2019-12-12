#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import argparse
from xml.sax import make_parser, handler

from settings import Settings
from note_parser import NoteParser

settings = Settings()


def run_parse():
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


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(prog='Evernote Dump',
                                         description='Evernote Dump exports and extracts evernote notes and '
                                                     'attachments from .enex files. All notes and attachments '
                                                     'will keep their original file created and accessed dates. '
                                                     'Notes will be converted to markdown format. Tags and other '
                                                     'embedded information will be formatted and added to the end '
                                                     'of each note. Evernote Dump works by streaming the .enex file '
                                                     'through a parser so even extremely large .enex files '
                                                     'should work. ')
    arg_parser.add_argument('enex', nargs='*',
                            help='Filename of exported Evernote .enex file. Multiple files or "*" wildcards can be '
                                 'used if your terminal supports wildcard expansion.')
    arg_parser.add_argument('-p', action='store_true',
                            help='Preserve original filenames for attachments.')
    arg_parser.parse_args(namespace=settings)

    print(settings.files)
    run_parse()


