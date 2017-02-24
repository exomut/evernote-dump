#!/usr/bin/env python
# -*- coding: utf-8 -*-

from helpers import *
import datetime

################
## Note Class ##
################

class Note(object):
    EVERNOTE_DATE_FORMAT = "%Y%m%dT%H%M%SZ"
    def __init__(self):
        # Extracted
        self.title = "CHANGE ME"
        self.html = ""
        self.created_date = ""
        self.updated_date = ""
        self.tags = []
        self.attributes = {}
        self.attr_latitude = None
        self.attr_longitude = None
        self.attr_altitude = None
        self.attr_author = None
        # Resources/Attachments
        self.attachments = []
        # Created
        self.filename = ""
        self.markdown = ""

    def append_html(self, text):
        self.html += text
    
    def append_to_notemd(self, text):
        """Adds a new line of text to the markdown version of the note"""
        self.notemd += "\n" + text

    def create_filename(self):
        self.filename = self.title[:100] + ".md"
        
    def finalize(self):
        """Output the note to a file"""
       
    def new_attachment(self, filename):
        self.attachments.append(Attachment(filename))
        
    def set_created(self, date_string):
        """Converts a date in string format to a datetime"""
        self.created_date = datetime.datetime.strptime(date_string, self.EVERNOTE_DATE_FORMAT)
        

######################
## ATTACHMENT CLASS ##
######################

import base64
import mimetypes # Converts mime file types into an extension

class Attachment(object):
    def __init__(self):
        """Take in encrypted data, un-encrypt it, save to a file, gather attributes"""
        self.filename = ""
        self.mime = ""
        self.base64data = ""
        self.rawdata = ""
        self.attributes = {}
    
    def add_found_attribute(self, attr, dataline):
        self.attributes[attr] = dataline

    def create_filename(self, keep_file_names):
        base = ""
        extension = ""
        if self.filename.count('.') >= 1:
            extension = self.filename.split('.')[-1]
            base = self.filename.rstrip('.' + extension)
        else:
            print(self.mime)
            extension = mimetypes.guess_extension(self.mime)
            extension = extension.replace('.jpe', '.jpg')
        
        if keep_file_names:
            # Limit filename length to 100 characters
            self.filename = base[:100] + '.' + extension
        else:
            self.filename = "somedate" # TODO

    def finalize(self, keep_file_names):
        self.create_filename(keep_file_names)
        self.decodeBase64()
        #TODO newFileName = checkForDouble(newFileName)    
        with open(makeDirCheck('Notes/media/') + self.filename,'wb') as outfile:
            outfile.write(self.rawdata)
        self.rawdata = ""
        
    def get_extention(self, mimetype):
        if filename.count('.') >= 1:
            return '.' + filename.split('.')[-1]
        else:
            extension = mimetypes.guess_extension(mimetype)
            return extension.replace('.jpe', '.jpg')

    def data_stream_in(self, dataline):
        self.base64data += dataline.rstrip('\n')
    
    def decodeBase64(self):
        ''' Decode base64 to memory '''
        try:
            self.rawdata = base64.b64decode(self.base64data)
            self.base64data = ""
        except TypeError:
            raise SystemExit

    def set_filename(self, filename):
        self.filename = filename

    def set_mime(self, mime):
        self.mime = mime
