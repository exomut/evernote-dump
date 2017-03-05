#!/usr/bin/env python
# -*- coding: utf-8 -*-

#############
## IMPORTS ##
#############

import sys
import xml.sax # Steaming XML data for use with larger files
from note import Note, Attachment
from helpers import isYesNo, chooseLanguage

############################
## Note Handler Functions ##
############################

class NoteHandler( xml.sax.ContentHandler ):
    def __init__(self):
        #self.html2text = html2text.HTML2Text()
        self.CurrentData = ""
        self.in_resource_attributes = False

    ########################
    ## ELEMENT READ START ##
    ########################
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
            self.attachment.set_created_date(self.note.get_created_date())
            self.attachment.set_filename(self.note.get_title())
        elif tag == "resource-attributes":
            self.in_resource_attributes = True
        
        
    
    #########################
    ## ELEMENT READ FINISH ##
    #########################
    def endElement(self, tag):
        if tag == "title":
            print("\nProcessing note: " + self.note.get_title())
        elif tag == "content":
            pass
        elif tag == "resource":
            self.attachment.finalize(keep_file_names)
            self.in_resource_attributes = False
            print("---Exported attachment: " + self.attachment.get_filename())
        elif tag == "data":
            self.note.add_attachment(self.attachment)
        elif tag == "note": # Last tag called before starting a new note
            #TODO ask user if they want to use qownnotes style. i.e. make attachment links "file://media/aldskfj.png"
            print("---Exporting note: " + self.note.get_filename())
            print("Finalizing note...")    
            self.note.finalize()
        elif tag == "en-export": #Last tag closed in the whole .enex file
            print("\n####EXPORT COMPLETE####\n")

    #########################
    ## CONTENT STREAM READ ##
    #########################
    def characters(self, content_stream):
        if self.CurrentData == "title":
            self.note.set_title(content_stream)
        elif self.CurrentData == "content":
            self.note.append_html(content_stream)
        elif self.CurrentData == "created":
            self.note.set_created_date(content_stream)
        elif self.CurrentData == "tag":
            self.note.append_tag(content_stream)
        elif self.CurrentData == "data":
            self.attachment.data_stream_in(content_stream)
        elif self.CurrentData == "mime":
            self.attachment.set_mime(content_stream)
        elif self.CurrentData == "file-name":
            self.attachment.set_filename(content_stream)
        
        if self.in_resource_attributes:
            self.attachment.add_found_attribute(self.CurrentData, content_stream)

if ( __name__ == "__main__"):

    #INIT Request user input
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
