#!/usr/bin/env python
# -*- coding: utf-8 -*-

from helpers import *
from datetime import datetime
import re # Regex module for extracting note attachments
import html2text # Convert html notes to markdown
import binascii


###########################
## Non-Handler Functions ##
###########################
def extractAttachment(self):

    ## fileName = datetime.datetime.strptime(self.created, __ISO_DATE_FORMAT).strftime(__TIME_FORMAT)
    newFileName = ''
    newFileName = checkForDouble(newFileName)    
    ## os.rename('temp/' + fileName, newFileName)

    # Set the date and time of the note to the file modified and access
    timeStamp = datetime.time.mktime(self.__created)
    os.utime(newFileName, (timeStamp, timeStamp))
    
    return newFileName

################
## Note Class ##
################
class Note(object):
    __NOTE_PATH = "Notes/"
    __MEDIA_PATH = "media/"
    __ISO_DATE_FORMAT = "%Y%m%dT%H%M%SZ"
    def __init__(self):
        self.html2text = html2text.HTML2Text()
        # Extracted
        self.__title = ""
        self.__html = ""
        self.__created_date = datetime.now()
        self.__updated_date = self.__created_date
        self.__tags = []
        self.__attributes = {}
        self.__attr_latitude = None
        self.__attr_longitude = None
        self.__attr_altitude = None
        self.__attr_author = None
        # Resources/Attachments
        self.__attachments = []
        # Created
        self.__filename = ""
        self.__markdown = ""

    def add_attachment(self, attachment):
        self.__attachments.append(attachment)

    def append_html(self, text):
        self.__html += text
        
    def append_tag(self, tag):
        self.__tags.append(tag)
    
    def append_to_notemd(self, text):
        """Adds a new line of text to the markdown version of the note"""
        self.__notemd += "\n" + text
        
    def clean_html(self):
        """Cleans self.__html and prepares it for markdown conversion."""
        # Find all attachment links in notes
        matches = re.findall(r'<en-media[^>]*\/>', self.__html)
        # Replace all attachments links with a placeholder
        for i in range(len(matches)):
            _hash = re.findall(r'[a-zA-Z0-9]{32}', matches[i])
            if_image = ""
            if "image" in matches[i]: if_image = "!"

            #self.__html = self.__html.replace(matches[i], '\n' + if_image + '[noteattachment' + str(i) + '][' + _hash[0] + ']')
            placeholder = "\n%s[noteattachment%d][%s]" % (if_image, i+1, _hash[0])
            self.__html = self.__html.replace(matches[i], placeholder)
        # Insert a title to be parsed in markdown
        self.__html = ("<h1>" + self.__title + "</h1>" + self.__html).encode('utf-8') 
        
        
    def create_filename(self):
        self.__filename = checkForDouble(makeDirCheck(self.__NOTE_PATH),  self.__title[:100] + ".md")    
    
    def create_markdown(self):
        self.clean_html()
        # Convert to markdown
        self.__markdown = self.html2text.handle(self.__html.decode('utf-8'))
        self.create_markdown_attachments()
        with open(self.__NOTE_PATH + self.__filename,'w') as outfile:
            outfile.write(self.__markdown)
            
    def create_markdown_attachments(self):
        """Appends the attachment information in markdown format to self.__markdown"""
        if len(self.__attachments) > 0:
            self.__markdown += "\n---"
            self.__markdown += "\n### ATTACHMENTS"
            for i in range(len(self.__attachments)):
                self.__markdown += "\n[%s]: %s%s" % (self.__attachments[i].get_hash(), self.__MEDIA_PATH, self.__attachments[i].get_filename())
                self.__markdown += self.__attachments[i].get_attributes()
        
    def finalize(self):
        """Output the note to a file"""
        self.create_markdown()

    def get_created_date(self):
        return self.__created_date
    
    def get_filename(self):
        return self.__filename

    def get_title(self):
        return self.__title

    def new_attachment(self, filename):
        self.__attachments.append(Attachment(filename))
        
    def set_created_date(self, date_string):
        self.__created_date = datetime.strptime(date_string, self.__ISO_DATE_FORMAT)
        
    def set_title(self, title):
        self.__title = title
        self.create_filename()
        

######################
## ATTACHMENT CLASS ##
######################

import base64
import mimetypes # Converts mime file types into an extension
import hashlib

class Attachment(object):
    __NOTE_PATH = "Notes/"
    __MEDIA_PATH = "media/"
    __NOTE_ATTATCHMENT_PATH = __NOTE_PATH + __MEDIA_PATH
    __TIME_FORMAT = "%Y-%m-%d_%H-%M-%S"
    def __init__(self):
        """Take in encrypted data, un-encrypt it, save to a file, gather attributes"""
        self.__created_date = datetime.now()
        self.__filename = ""
        self.__mime = ""
        self.__base64data = ""
        self.__rawdata = ""
        self.__attributes = []
    
    def add_found_attribute(self, attr, dataline):
        self.__attributes.append([attr, dataline])

    def create_filename(self, keep_file_names):
        __base = self.__filename
        __extension = ""

        if self.__filename.count('.') >= 1:
            __extension = self.__filename.split('.')[-1]
            __base = self.__filename.rstrip('.' + __extension)
        else:
            """Create an extension if no original filename found."""
            __extension = mimetypes.guess_extension(self.__mime, False)[1:]
            if __extension == "jpe":
                __extension = "jpg"

        if keep_file_names and __base:
            # Limit filename length to 100 characters
            self.__filename = __base[:100] + '.' + __extension
        else:
            self.__filename = self.__created_date.strftime(self.__TIME_FORMAT) + '.' + __extension
        
        self.__filename = self.__filename.replace(" ", "_")
        self.__filename = checkForDouble(self.__NOTE_ATTATCHMENT_PATH,  self.__filename)    

    def finalize(self, keep_file_names):
        self.create_filename(keep_file_names)
        self.decodeBase64()
        __path = makeDirCheck(self.__NOTE_ATTATCHMENT_PATH) + self.__filename
        with open(__path,'wb') as outfile:
            outfile.write(self.__rawdata)
        md5 = hashlib.md5()
        md5.update(self.__rawdata)
        self.__hash = binascii.hexlify(md5.digest()).decode()
        os.utime(__path, (self.__created_date.timestamp(), self.__created_date.timestamp()))
        self.__rawdata = ""
        
    def get_attributes(self):
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

    def data_stream_in(self, dataline):
        self.__base64data += dataline.rstrip('\n')
    
    def decodeBase64(self):
        ''' Decode base64 to memory '''
        try:
            self.__rawdata = base64.b64decode(self.__base64data)
            self.__base64data = ""
        except TypeError:
            raise SystemExit

    def set_created_date(self, created_date):
        self.__created_date = created_date

    def set_filename(self, filename):
        self.__filename = filename

    def set_mime(self, mime):
        self.__mime = mime
