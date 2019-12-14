#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import sys


from gui import load_gui
from dump import run_parse
from utilities.settings import Settings

if __name__ == "__main__":
    settings = Settings()
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

    if len(sys.argv) == 1:
        load_gui()
    else:
        run_parse(settings)
