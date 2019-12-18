#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from xml.sax import ContentHandler

from utilities.settings import Settings
from .note import Note, Attachment


class NoteParser(ContentHandler):
    """
    Handles all lines of the enex file in a streaming manner.
    Large files can be parsed since it is not loaded to memory.

    :param current_file
    :param settings: Settings is a custom class to pass application wide settings.
    :param print_fun: func Pass in a callback function that will be passed a string for printing
        and disable printing to console.
    """

    def __init__(self, current_file, settings: Settings, print_func=None):
        super().__init__()
        self.settings = settings
        self.print_func = print_func

        self.current_file = current_file

        self.CurrentData = ""
        self.in_note_attributes = False
        self.in_resource_attributes = False
        self.note = None
        self.attachment = None
        self.path = settings.export_path

    def print_message(self, message: str):
        if self.print_func:
            self.print_func(message)
        else:
            print(message)

    def startElement(self, tag, attributes):
        """ Called when a new element is found """
        self.CurrentData = tag
        if tag == "en-export":  # First tag found in .enex file
            self.print_message("\n####EXPORT STARTED####")
        elif tag == "note":  # New note found
            self.note = Note()
            self.note.set_path(os.path.join(self.path, self.current_file))
        elif tag == "resource":  # Found an attachment
            self.attachment = Attachment()
            self.attachment.set_path(os.path.join(self.path, self.current_file))
            self.attachment.set_created_date(self.note.get_created_date())
            self.attachment.set_filename(self.note.get_title())
            self.attachment.set_uuid(self.note.get_uuid())
        elif tag == "note-attributes":
            self.in_note_attributes = True
        elif tag == "resource-attributes":
            self.in_resource_attributes = True

    def endElement(self, tag):
        """Called at the end of an element"""
        if tag == "title":
            self.print_message(f"\nProcessing Note: {self.note.get_title()}")
        elif tag == "content":
            pass
        elif tag == "resource":
            self.print_message(f"---Exporting Attachment: {self.attachment.get_filename()}")
            try:
                self.attachment.finalize(self.settings.preserve_file_names)
            except NameError:
                self.attachment.finalize(True)
            self.in_resource_attributes = False
        elif tag == "data":
            self.note.add_attachment(self.attachment)
        elif tag == "note":  # Last tag called before starting a new note
            self.print_message(f"---Exporting Note: {self.note.get_filename()}")
            self.note.finalize()
        elif tag == "note-attributes":
            self.in_note_attributes = False
        elif tag == "en-export":  # Last tag closed in the whole .enex file
            self.print_message("\n####EXPORT FINISHED####\n")

    def characters(self, content_stream):
        """Content Stream"""
        if self.CurrentData == "title":
            self.note.set_title(content_stream)
        elif self.CurrentData == "content":
            self.note.append_html(content_stream)
        elif self.CurrentData == "created":
            self.note.set_created_date(content_stream)
        elif self.CurrentData == "updated":
            self.note.set_updated_date(content_stream)
        elif self.CurrentData == "tag":
            self.note.append_tag(content_stream)
        elif self.CurrentData == "data":
            self.attachment.data_stream_in(content_stream)
        elif self.CurrentData == "mime":
            self.attachment.set_mime(content_stream)
        elif self.CurrentData == "file-name":
            self.attachment.set_filename(content_stream)

        if self.in_note_attributes:
            self.note.add_found_attribute(self.CurrentData, content_stream)
        if self.in_resource_attributes:
            self.attachment.add_found_attribute(self.CurrentData, content_stream)
