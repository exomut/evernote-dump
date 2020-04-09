#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re  # Regex module for extracting note attachments
import uuid
from datetime import datetime

import html2text  # Convert html notes to markdown
from bs4 import BeautifulSoup

from note_parser.attachment import Attachment
from utilities.tool_kit import *


class Note(object):
    """
    Note Class organizes and exports all parsed data and exports to a markdown file.
    """

    MEDIA_PATH = "media/"
    ISO_DATE_FORMAT = "%Y%m%dT%H%M%SZ"
    TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

    def __init__(self):
        self.html2text = html2text.HTML2Text()
        self.html2text.drop_white_space = 1
        self.html2text.wrap_links = False
        self.html2text.body_width = 0
        self.html2text.wrap_list_items = False
        self.html2text.single_line_break = True

        # Extracted
        self._title = ""
        self._html = ""
        self._created_date = datetime.now()
        self._updated_date = self._created_date
        self._tags = []
        self._attributes = []
        self._path = ""
        # Resources/Attachments
        self._attachments = []
        # Created
        self._filename = ""
        self._markdown = ""
        self._uuid = uuid.uuid4()

    def add_attachment(self, attachment):
        self._attachments.append(attachment)

    def add_found_attribute(self, attr, dataline):
        self._attributes.append([attr, dataline])

    def append_html(self, text):
        self._html += text

    def append_tag(self, tag):
        self._tags.append(tag)

    def clean_html(self):
        # Cleans self.__html and prepares it for markdown conversion.
        self.convert_code_blocks()
        self.convert_evernote_markings()

        # Remove troublesome 'divs' from tables
        for match in re.findall(r"<tbody>.*?<\/tbody>", self._html):
            self._html = self._html.replace(match, "[evernote-dump-table-cleaner]")
            match = match.replace("<div><br/></div>", "")
            for div in re.findall(r"<div>(?!<div>).*?<\/div>", match):
                clean_div = div.replace("<div>", "").replace("</div>", "")
                match = match.replace(div, clean_div)
            self._html = self._html.replace("[evernote-dump-table-cleaner]", match)

        # Insert a title to be parsed in markdown
        self._html = ("<h1>" + self._title + "</h1>" + self._html).encode('utf-8')

    def convert_evernote_markings(self):
        self.convert_evernote_markings_attachments()

        replacements = (
            # Handle Checkboxes
            # without this workaround html2text will convert '-' to '\\-' because there is space after dash
            ('<en-todo checked="false"/>', '-<ignore> [ ] '),
            ('<en-todo checked="false">', '-<ignore> [ ] '),
            ('<en-todo checked="true"/>', '-<ignore> [x] '),
            ('<en-todo checked="true">', '-<ignore> [x] '),
            ('</en-todo>', ''),
        )

        for take, give in replacements:
            self._html = self._html.replace(take, give)

    def convert_code_blocks(self):
        soup = BeautifulSoup(self._html, "html.parser")
        code_block = re.compile(r"-en-codeblock:true")
        for block in soup.findAll("div", style=code_block):
            block.insert_before('```')
            block.insert_after('```')
        self._html = str(soup)

    def convert_evernote_markings_attachments(self):
        # Find all attachment links in notes
        matches = re.findall(r'<en-media.*?>', self._html)

        # Replace all attachments links with a hash placeholder
        for i in range(len(matches)):
            _hash = re.findall(r'[a-zA-Z0-9]{32}', matches[i])
            if_image = "!" if "image" in matches[i] else ""
            placeholder = "\n%s[noteattachment%d][%s]" % (if_image, i + 1, _hash[0])
            self._html = self._html.replace(matches[i], placeholder)

    def convert_html_to_markdown(self):
        self._markdown = self.html2text.handle(self._html.decode('utf-8'))

    def create_file(self):
        with open(os.path.join(self._path, self._filename), 'w', encoding='UTF-8', errors='replace') as outfile:
            outfile.write(self._markdown)
        os.utime(os.path.join(self._path, self._filename),
                 (self._created_date.timestamp(), self._updated_date.timestamp()))

    def create_filename(self):
        # make sure title can be converted to filename
        if not any(char.isalpha() or char.isdigit() for char in self._title):
            self._title = "_" + str(self._uuid)

        self._filename = check_for_double(make_dir_check(self._path), path_safe_string(self._title[:128]) + ".md")

    def create_placeholders(self):
        # Create place holder to preserve spaces and tabs
        self._html = self._html.replace("&nbsp; &nbsp; ", "[endumptab]")
        self._html = self._html.replace("&nbsp;", "[endumpspace]")

    def restore_placeholders(self):
        self._markdown = self._markdown.replace("[endumptab]", "\t")
        self._markdown = self._markdown.replace("[endumpspace]", " ")

    def clean_markdown(self):
        self._markdown = '\n'.join([line.rstrip() for line in self._markdown.splitlines()])

    def create_markdown(self):
        self.create_placeholders()
        self.clean_html()
        self.convert_html_to_markdown()
        self.restore_placeholders()
        self.create_markdown_attachments()
        if len(self._tags) > 0:
            self.create_markdown_note_tags()
        self.create_markdown_note_attr()
        self.clean_markdown()
        self.create_file()

    def create_markdown_attachments(self):
        # Appends the attachment information in markdown format to self.__markdown
        if len(self._attachments) > 0:
            self._markdown += "\n---"
            self._markdown += "\n### ATTACHMENTS"
            for i in range(len(self._attachments)):
                self._markdown += "\n[%s]: %s%s" % (
                    self._attachments[i].get_hash(), self.MEDIA_PATH, self._attachments[i].get_filename())
                self._markdown += self._attachments[i].get_attributes()

    def create_markdown_note_attr(self):
        self._markdown += "\n---"
        self._markdown += "\n### NOTE ATTRIBUTES"
        self._markdown += "\n>Created Date: " + self._created_date.strftime(self.TIME_FORMAT) + "  "
        self._markdown += "\n>Last Evernote Update Date: " + self._updated_date.strftime(self.TIME_FORMAT) + "  "
        if len(self._attributes) > 0:
            for attr in self._attributes:
                self._markdown += "\n>%s: %s  " % (attr[0], attr[1])

    def create_markdown_note_tags(self):
        self._markdown += "\n\n---"
        self._markdown += "\n### TAGS\n"
        tags = '  '.join(['{%s}' % tag for tag in self._tags])
        tags += "\n"
        self._markdown += tags

    def finalize(self):
        self.create_markdown()

    def get_created_date(self):
        return self._created_date

    def get_filename(self):
        return self._filename

    def get_title(self):
        return self._title

    def get_uuid(self):
        return self._uuid

    def new_attachment(self):
        self._attachments.append(Attachment())

    def set_created_date(self, date_string):
        try:
            self._created_date = datetime.strptime(date_string, self.ISO_DATE_FORMAT)
        except (TypeError, ValueError):
            self._created_date = datetime.now()

    def set_updated_date(self, date_string):
        try:
            self._updated_date = datetime.strptime(date_string, self.ISO_DATE_FORMAT)
        except (TypeError, ValueError):
            self._created_date = datetime.now()

    def set_path(self, path):
        self._path = path

    def set_title(self, title):
        self._title = title
        self.create_filename()
