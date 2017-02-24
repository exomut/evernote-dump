#!/usr/bin/env python
# -*- coding: utf-8 -*-

#############
## IMPORTS ##
#############

import xml.sax # Steaming XML data for use with larger files
import os
import re # Regex module for extracting note attachments
import sys
import datetime
import magic
import html2text # Convert html notes to markdown

from note import Note, Attachment
from helpers import *

############################
## Note Handler Functions ##
############################

class NoteHandler( xml.sax.ContentHandler ):
    def __init__(self):
        try:
            self.magic = magic.Magic(flags=magic.MAGIC_MIME_TYPE)
        except AttributeError:
            self.magic = magic.Magic(mime=True)
        self.html2text = html2text.HTML2Text()
        self.CurrentData = ""

    def startElement(self, tag, attributes):
        '''
        Called when a new element is found
        '''
        self.CurrentData = tag
        if tag == "en-export": # First tag found in .enex file
            print("\n####EXPORT STARTED####")
        elif tag == "note": # New note found
            self.note = Note()
        elif tag == "data": # Found an attachment
            self.attachment = Attachment()
            self.attachment.set_filename(self.note.title)
            print("---Exporting attachment: ")
    
    def endElement(self, tag):
        if tag == "title":
            print("\nProcessing note: " + self.note.title)
        elif tag == "content":
            print("---Exporting note: " + self.note.filename)
        elif tag == "resource":
            self.attachment.finalize(keep_file_names)
        elif tag == "data":
            self.note.attachments.append(self.attachment)
        elif tag == "note": # Last tag called before starting a new note
            #TODO ask user if they want to use qownnotes style. i.e. make attachment links "file://media/aldskfj.png"
            print("Finalizing note...")    
        elif tag == "en-export": #Last tag closed in the whole .enex file
            self.magic.close()
            print("\n####EXPORT COMPLETE####\n")

    def characters(self, content_stream):
        if self.CurrentData == "title":
            self.note.title = content_stream
        elif self.CurrentData == "content":
            self.note.append_html(content_stream)
        elif self.CurrentData == "created":
            self.note.set_created(content_stream)
        elif self.CurrentData == "data":
            self.attachment.data_stream_in(content_stream)
        elif self.CurrentData == "mime":
            self.attachment.set_mime(content_stream)
        elif self.CurrentData == "file-name":
            self.attachment.set_filename(content_stream)

###########################
## Non-Handler Functions ##
###########################
def extractAttachment(self):

    fileName = datetime.datetime.strptime(self.created, "%Y%m%dT%H%M%SZ").strftime("%Y-%m-%d_%H-%M-%S")
    newFileName = ''
    newFileName = checkForDouble(newFileName)    
    os.rename('temp/' + fileName, newFileName)

    # Set the date and time of the note to the file modified and access
    timeStamp = datetime.time.mktime(datetime.time.strptime(self.created, "%Y%m%dT%H%M%SZ"))
    os.utime(newFileName, (timeStamp, timeStamp))
    
    return newFileName

if ( __name__ == "__main__"):
    
    chooseLanguage()
    keep_file_names = isYesNo('Would you like to keep the original filenames if found?')

    # create an XMLReader
    parser = xml.sax.make_parser()

    # turn off namespaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    #override the default ContextHandler
    Handler = NoteHandler()
    parser.setContentHandler( Handler )
    
    # pass in first argument as input file.
    parser.parse(sys.argv[1])
