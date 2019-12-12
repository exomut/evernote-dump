#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
import os
import shutil

from evernote_dump import evernote_dump
from settings import Settings


class TestEvernoteDump(unittest.TestCase):

    def setUp(self) -> None:
        self.s = Settings()
        evernote_dump.settings = self.s

    def test_run_parse_single_file_with_out_overwrite(self):
        self.s.files = ['../data/Archives.enex']

        evernote_dump.run_parse()
        self.assertTrue(os.path.isdir('Archives'))
        shutil.rmtree('Archives')

    def test_run_parse_auto_rename_do_not_overwrite(self):
        self.s.files =['../data/Check It Out.enex', '../data/Check It Out.enex']
        evernote_dump.run_parse()
        evernote_dump.run_parse()
        self.assertTrue(os.path.isdir('Check It Out'))
        self.assertTrue(os.path.isfile('Check It Out/Great Chili-2.md'))
        shutil.rmtree('Check It Out')

    def test_run_parse_multiple_files(self):
        self.s.files =['../data/Archives.enex', '../data/Recipes.enex']
        evernote_dump.run_parse()
        self.assertTrue(os.path.isdir('Archives'))
        self.assertTrue(os.path.isdir('Recipes'))
        shutil.rmtree('Archives')
        shutil.rmtree('Recipes')

    def test_run_parse_with_spaces_in_file_name(self):
        self.s.files = ['../data/Check It Out.enex', ]
        evernote_dump.run_parse()
        self.assertTrue(os.path.isdir('Check It Out'))
        shutil.rmtree('Check It Out')


if __name__ == '__main__':
    unittest.main()
