#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Settings:

    def __init__(self):
        self.files = []
        self.export_path = ""
        self.preserve_file_names = False
        self.use_note_title_for_attachments = False

    @property
    def path(self):
        return self.export_path

    @path.setter
    def path(self, path: str):
        self.export_path = path

    @property
    def p(self):
        return self.preserve_file_names

    @p.setter
    def p(self, p: bool):
        self.preserve_file_names = p

    @property
    def n(self):
        return self.use_note_title_for_attachments

    @n.setter
    def n(self, n: bool):
        self.use_note_title_for_attachments = n

    @property
    def enex(self):
        return self.files

    @enex.setter
    def enex(self, files: list):
        for file in files:
            if '.enex' in file:
                self.files.append(file)

