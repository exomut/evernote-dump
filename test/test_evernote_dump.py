#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
import os
import shutil

from evernote_dump import dump
from utilities.settings import Settings


class TestEvernoteDump(unittest.TestCase):

    def setUp(self) -> None:
        self.s = Settings()

    # TODO: Add test for preserved file names

    def test_run_parse_single_file_with_out_overwrite(self):
        self.s.files = ['../data/Archives.enex']
        dump.run_parse(self.s)
        self.assertTrue(os.path.isdir('Archives'))
        shutil.rmtree('Archives')

    def test_run_parse_auto_rename_do_not_overwrite(self):
        self.s.files =['../data/Check It Out.enex', '../data/Check It Out.enex']
        dump.run_parse(self.s)
        dump.run_parse(self.s)
        self.assertTrue(os.path.isdir('Check It Out'))
        self.assertTrue(os.path.isfile('Check It Out/Great Chili-2.md'))
        shutil.rmtree('Check It Out')

    def test_run_parse_multiple_files(self):
        self.s.files =['../data/Archives.enex', '../data/Recipes.enex']
        dump.run_parse(self.s)
        self.assertTrue(os.path.isdir('Archives'))
        self.assertTrue(os.path.isdir('Recipes'))
        shutil.rmtree('Archives')
        shutil.rmtree('Recipes')

    def test_run_parse_with_spaces_in_file_name(self):
        self.s.files = ['../data/Check It Out.enex', ]
        dump.run_parse(self.s)
        self.assertTrue(os.path.isdir('Check It Out'))
        shutil.rmtree('Check It Out')


if __name__ == '__main__':
    unittest.main()
