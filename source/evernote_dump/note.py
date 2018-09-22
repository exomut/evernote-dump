#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .helpers import *
from datetime import datetime
import re  # Regex module for extracting note attachments
import html2text  # Convert html notes to markdown
import uuid


##############
# Note Class #
##############
class Note(object):
    __MEDIA_PATH = "media/"
    __ISO_DATE_FORMAT = "%Y%m%dT%H%M%SZ"
    __TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

    def __init__(self):
        self.html2text = html2text.HTML2Text()
        # Extracted
        self.__title = ""
        self.__html = ""
        self.__created_date = datetime.now()
        self.__updated_date = self.__created_date
        self.__tags = []
        self.__attributes = []
        self.__path = ""
        # Resources/Attachments
        self.__attachments = []
        # Created
        self.__filename = ""
        self.__markdown = ""
        self.__uuid = uuid.uuid4()

    def add_attachment(self, attachment):
        self.__attachments.append(attachment)

    def add_found_attribute(self, attr, dataline):
        self.__attributes.append([attr, dataline])

    def append_html(self, text):
        self.__html += text
        
    def append_tag(self, tag):
        self.__tags.append(tag)
    
    def append_to_notemd(self, text):
        # Adds a new line of text to the markdown version of the note
        self.__notemd += "\n" + text
        
    def clean_html(self):
        # Cleans self.__html and prepares it for markdown conversion.
        self.convert_evernote_markings()

        # Insert a title to be parsed in markdown
        self.__html = ("<h1>" + self.__title + "</h1>" + self.__html).encode('utf-8') 
        
    def convert_evernote_markings(self):
        self.convert_evernote_markings_attachments()

        replacements = (
            # Handle Checkboxes
            ('<en-todo checked="false"/>', '-<ignore> [ ] '),    # without this hack html2text will convert '-' to '\\-' because there is space after dash
            ('<en-todo checked="false">', '-<ignore> [ ] '),
            ('<en-todo checked="true"/>', '-<ignore> [x] '),
            ('<en-todo checked="true">', '-<ignore> [x] '),
            ('</en-todo>', ''),
        )

        for take, give in replacements:
            self.__html = self.__html.replace(take, give)
        
    def convert_evernote_markings_attachments(self):
        # Find all attachment links in notes
        matches = re.findall(r'<en-media[^>]*\/>', self.__html)
        # Replace all attachments links with a hash placeholder
        for i in range(len(matches)):
            _hash = re.findall(r'[a-zA-Z0-9]{32}', matches[i])
            if_image = "!" if "image" in matches[i] else "!"
            placeholder = "\n%s[noteattachment%d][%s]" % (if_image, i+1, _hash[0])
            self.__html = self.__html.replace(matches[i], placeholder)

    def convert_html_to_markdown(self):
        self.__markdown = self.html2text.handle(self.__html.decode('utf-8'))
		
    def create_file(self):
        with open(os.path.join(self.__path, self.__filename), 'w', encoding='UTF-8', errors='replace') as outfile:
            outfile.write(self.__markdown)
        os.utime(os.path.join(self.__path, self.__filename), (self.__created_date.timestamp(), self.__updated_date.timestamp()))

    def create_filename(self):
        self.__filename = check_for_double(make_dir_check(self.__path),  url_safe_string(self.__title[:128]) + ".md")
    
    def create_markdown(self):
        self.clean_html()
        self.convert_html_to_markdown()
        self.create_markdown_attachments()
        if len(self.__tags) > 0:
            self.create_markdown_note_tags()
        self.create_markdown_note_attr()
        self.create_file()
            
    def create_markdown_attachments(self):
        # Appends the attachment information in markdown format to self.__markdown
        if len(self.__attachments) > 0:
            self.__markdown += "\n---"
            self.__markdown += "\n### ATTACHMENTS"
            for i in range(len(self.__attachments)):
                self.__markdown += "\n[%s]: %s%s" % (self.__attachments[i].get_hash(), self.__MEDIA_PATH, self.__attachments[i].get_filename())
                self.__markdown += self.__attachments[i].get_attributes()
                
    def create_markdown_note_attr(self):
        self.__markdown += "\n---"
        self.__markdown += "\n### NOTE ATTRIBUTES"
        self.__markdown += "\n>Created Date: " + self.__created_date.strftime(self.__TIME_FORMAT) + "  "
        self.__markdown += "\n>Last Evernote Update Date: " + self.__updated_date.strftime(self.__TIME_FORMAT) + "  "
        if len(self.__attributes) > 0:
            for attr in self.__attributes:
                self.__markdown += "\n>%s: %s  " % (attr[0], attr[1])
        
    def create_markdown_note_tags(self):
        self.__markdown += "\n\n---"
        self.__markdown += "\n### TAGS\n"
        tags = '  '.join(['{%s}' % tag for tag in self.__tags])
		tags += "\n"
        self.__markdown += tags

    def finalize(self):
        self.create_markdown()

    def get_created_date(self):
        return self.__created_date
    
    def get_filename(self):
        return self.__filename

    def get_title(self):
        return self.__title
    
    def get_uuid(self):
        return self.__uuid

    def new_attachment(self, filename):
        self.__attachments.append(Attachment(filename))
        
    def set_created_date(self, date_string):
        self.__created_date = datetime.strptime(date_string, self.__ISO_DATE_FORMAT)
    
    def set_updated_date(self, date_string):
        self.__updated_date = datetime.strptime(date_string, self.__ISO_DATE_FORMAT)

    def set_path(self, path):
        self.__path = path
        
    def set_title(self, title):
        self.__title = title
        self.create_filename()
        
####################
# ATTACHMENT CLASS #
####################

import base64  # Decodes base64
import mimetypes  # Converts mime file types into an extension
import hashlib  # Used to get md5 hash from attachments
import binascii  # Used to convert hash output to string


class Attachment(object):
    __MEDIA_PATH = "media/"
    __TIME_FORMAT = "%Y-%m-%d_%H-%M-%S"

    def __init__(self):
        """Take in encrypted data, un-encrypt it, save to a file, gather attributes"""
        self.__created_date = datetime.now()
        self.__filename = ""
        self.__mime = ""
        self.__base64data = []
        self.__rawdata = ""
        self.__attributes = []
        self.__path = ""
    
    def add_found_attribute(self, attr, dataline):
        self.__attributes.append([attr, dataline])

    def create_file(self):
        # Create the file and set the original timestamps
        __path = os.path.join(make_dir_check(os.path.join(self.__path, self.__MEDIA_PATH)), self.__filename)
        with open(__path,'wb') as outfile:
            outfile.write(self.__rawdata)
        os.utime(__path, (self.__created_date.timestamp(), self.__created_date.timestamp()))
        self.__rawdata = ""
        
    def create_filename(self, keep_file_names):
        __base = self.__filename

        if self.__filename.count('.') >= 1:
            __extension = self.__filename.split('.')[-1]
            __base = self.__filename.rstrip('.' + __extension)
        else:
            # Create an extension if no original filename found.
            __extension = mimetypes.guess_extension(self.__mime, False)[1:]
            if __extension == "jpe":
                __extension = "jpg"

        if keep_file_names and __base:
            # Limit filename length to 128 characters
            self.__filename = url_safe_string(__base[:128]) + '.' + __extension
        else:
            # Create a filename from created date if none found or unwanted
            self.__filename = self.__created_date.strftime(self.__TIME_FORMAT) + '.' + __extension
        
        # Remove spaces from filenames since markdown links won't work with spaces
        self.__filename = self.__filename.replace(" ", "_")
        
        # Try the filename and if a file with the same name exists add a counter to the end
        self.__filename = check_for_double(os.path.join(self.__path, self.__MEDIA_PATH),  self.__filename)
        
    def create_hash(self):
        md5 = hashlib.md5()
        md5.update(self.__rawdata)
        self.__hash = binascii.hexlify(md5.digest()).decode()

    def finalize(self, keep_file_names):
        try:
            self.create_filename(keep_file_names)
        except NameError:
            self.create_filename(True)
        self.decodeBase64()
        self.create_hash()
        self.create_file()
        
    def get_attributes(self):
        # Create a string of markdown code neatly formatted for all attributes
        export = "\n[%s](%s%s)" % (self.__filename, self.__MEDIA_PATH, self.__filename)
        if len(self.__attributes) > 0:
            export += "\n>hash: %s  " % (self.__hash)
            for attr in self.__attributes:
                export += "\n>%s: %s  " % (attr[0], attr[1])
            export +=  "\n"
        return export

    def get_extention(self, mimetype):
        if self.__filename.count('.') >= 1:
            return '.' + self.__filename.split('.')[-1]
        else:
            extension = mimetypes.guess_extension(mimetype)
            return extension.replace('.jpe', '.jpg')
        
    def get_filename(self):
        return self.__filename
    
    def get_hash(self):
        return self.__hash
    
    def get_uuid(self):
        return self.__uuid

    def data_stream_in(self, dataline):
        self.__base64data.append(dataline.rstrip('\n'))
    
    def decodeBase64(self):
        # Decode base64 image to memory
        try:
            self.__rawdata = base64.b64decode(''.join(self.__base64data))
            self.__base64data = []
        except TypeError:
            raise SystemExit

    def set_created_date(self, created_date):
        self.__created_date = created_date

    def set_filename(self, filename):
        self.__filename = filename

    def set_mime(self, mime):
        self.__mime = mime
    
    def set_path(self, path):
        self.__path = path
        
    def set_uuid(self, uuid):
        self.__uuid = uuid
