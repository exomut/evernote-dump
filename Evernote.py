#!/usr/bin/env python
# -*- coding: utf-8 -*-

keepFileNames = False

import xml.sax # Steaming XML data for use with larger files
import os
import re # Regex module for extracting note attachments
import sys
import mimetypes # Converts mime file types into an extension
import time # Used to set the modified and access time of the file
import datetime
import imp
import magic
import html2text # Convert html notes to markdown
from functions import *

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

    # New element found
    # Work with attributes such as: <en-media hash="kasd92">
    def startElement(self, tag, attributes):
        '''
        Called when a new element is found
        '''
        self.CurrentData = tag
        if tag == "en-export": # First tag found in .enex file
            print("\n####EXPORT STARTED####")
        elif tag == "note": # New note found
            self.title = ""
            self.note = ""
            self.notemd = ""
            self.filename = ""
            self.attachfilename = ""
            self.attachfilenames = []
            self.timestamp = ""
            self.dataCounter = 0
        elif tag == "content":
            self.note == ""
        elif tag == "en-media":
            hash = attributes["hash"]
        elif tag == "data": # Found an attachment
            self.file = open(makeDirCheck('temp') + '/temp.enc', 'wa')

    # When an element has finished reading this is called.
    # Process the collected data
    def endElement(self, tag):
        if tag == "title":
            print("\nProcessing note: " + self.title)
        elif tag == "content":
            makeNote(self)
            print("---Exporting note: " + self.filename)
        elif tag == "resource":
            # Extract all the attachements and get a list of extracted filenames
            self.attachfilenames.append(extractAttachment(self))
            print("---Exporting attachment: " + self.attachfilenames[len(self.attachfilenames)-1])
        elif tag == "data":
            self.file.close()
        elif tag == "note": # Last tag called before starting a new note
#TODO ask user if they want to use qownnotes style. i.e. make attachment links "file://media/aldskfj.png"
            writeNote(self)
            print("Finalizing note...")    
        elif tag == "en-export": #Last tag closed in the whole .enex file
            self.magic.close()
            print("\n####EXPORT COMPLETE####\n")

    def characters(self, content):
        if self.CurrentData == "title":
            self.title += content
        elif self.CurrentData == "content":
            self.note += content.encode('utf-8')
        elif self.CurrentData == "created":
            self.created = content
        elif self.CurrentData == "data":
            # Remove linebreaks added in the enex file to prepare for decoding
            self.file.write(content.rstrip('\n'))
        elif self.CurrentData == "timestamp":
            self.timestamp = content
        elif self.CurrentData == "file-name":
            self.attachfilename = content

###########################
## Non-Handler Functions ##
###########################

def extractAttachment(self):
    # I tried directly converting from memory, but it was too slow.
    # Converting from a temp file sped up the process
    self.file = open('temp/temp.enc', 'r')

    fileName = datetime.datetime.strptime(self.created, "%Y%m%dT%H%M%SZ").strftime("%Y-%m-%d_%H-%M-%S")
    decodeBase64(self.file.read(), fileName)
    self.file.close()    
    newFileName = ''
    if self.attachfilename and keepFileNames:
        newFileName = makeDirCheck('Notes/media/') + makeFileTitle(self.attachfilename)
    else:
        # Check the file for filetype and add the correct extension
        # I tried using Evernote's Mime-Types but some png files were marked as jpg
        mime = None
        try:
            mime = self.magic.id_filename('temp/' + fileName)
        except AttributeError:
            mime = self.magic.from_file('temp/' + fileName)

        self.extension = mimetypes.guess_extension(mime)
        self.extension = self.extension.replace('.jpe', '.jpg')
        newFileName = makeDirCheck('Notes/media/') + fileName + self.extension
    newFileName = checkForDouble(newFileName)    
    os.rename('temp/' + fileName, newFileName)

    # Set the date and time of the note to the file modified and access
    timeStamp = time.mktime(time.strptime(self.created, "%Y%m%dT%H%M%SZ"))
    os.utime(newFileName, (timeStamp, timeStamp))

    # Clean up temp files
    os.remove('temp/temp.enc')
    self.timestamp == ""
    self.attachfilename == ""
    
    return newFileName

def makeNote(self):
    self.filename = makeDirCheck('Notes') + '/' + makeFileTitle(self.title) + '.md'
    # Find all attachment links in notes
    matches = re.findall(r'<en-media[^>]*\/>', self.note)
    # Replace all attachments links with a placeholder
    for i in range(len(matches)):
        self.note = self.note.replace(matches[i], "<img src='evernote-dump-file-place-marker" + str(i) + "' />")
    # Insert a title to be parsed in markdown
    self.note = ("<h1>" + self.title + "</h1>" + self.note.decode('utf-8')).encode('utf-8')
    # Convert to markdown
    self.notemd = self.html2text.handle(self.note.decode('utf-8')).encode('utf-8')

def writeNote(self):
    with file(self.filename,'wb') as outfile:
        outfile.write(self.notemd)
        outfile.close()

def makeFileTitle(title):
        '''
        title: original title from note

        returns: limited to 100 characters and hyphenated
        '''
        return title[0:100]

if ( __name__ == "__main__"):
    
    chooseLanguage()
    keepFileNames = isYesNo('Would you like to keep the original filenames if found?')

    # create an XMLReader
    parser = xml.sax.make_parser()

    # turn off namespaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    #override the default ContextHandler
    Handler = NoteHandler()
    parser.setContentHandler( Handler )
    
    # pass in first argument as input file.
    parser.parse(sys.argv[1])
