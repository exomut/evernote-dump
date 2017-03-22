#!/usr/bin/env python
# -*- coding: utf-8 -*-

#############
## IMPORTS ##
#############

import sys
import xml.sax # Steaming XML data for use with larger files
from note import Note, Attachment
from helpers import isYesNo, chooseLanguage, lang, isPythonThree

############################
## Note Handler Functions ##
############################

class NoteHandler( xml.sax.ContentHandler ):
    def __init__(self):
        self.CurrentData = ""
        self.in_note_attributes = False
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
            print("\n####%s####" % (lang("_export_started")))
        elif tag == "note": # New note found
            self.note = Note()
            self.note.set_path(current_file)
        elif tag == "data": # Found an attachment
            self.attachment = Attachment()
            self.attachment.set_path(current_file)
            self.attachment.set_created_date(self.note.get_created_date())
            self.attachment.set_filename(self.note.get_title())
            self.attachment.set_uuid(self.note.get_uuid())
        elif tag == "note-attributes":
            self.in_note_attributes = True
        elif tag == "resource-attributes":
            self.in_resource_attributes = True
    
    #########################
    ## ELEMENT READ FINISH ##
    #########################
    def endElement(self, tag):
        if tag == "title":
            print("\n%s: %s" % ( lang('_note_processing'), self.note.get_title()))
        elif tag == "content":
            pass
        elif tag == "resource":
            print("---%s: %s" % (lang('_exporting_attachment'), self.attachment.get_filename()))
            self.attachment.finalize(keep_file_names)
            self.in_resource_attributes = False
        elif tag == "data":
            self.note.add_attachment(self.attachment)
        elif tag == "note": # Last tag called before starting a new note
            #TODO ask user if they want to use qownnotes style. i.e. make attachment links "file://media/aldskfj.png"
            print("---%s: %s" % (lang('_exporting_note'), self.note.get_filename()))
            self.note.finalize()
        elif tag == "note-attributes":
            self.in_note_attributes = False
        elif tag == "en-export": #Last tag closed in the whole .enex file
            print("\n####%s####\n" % (lang('_export_finished')))

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

if ( __name__ == "__main__"):
    
    if not isPythonThree():
        print("Please use Python version 3")
        sys.exit()

    #INIT Request user input
    chooseLanguage()
    keep_file_names = isYesNo('_keep_file_names_q')

    # create an XMLReader
    parser = xml.sax.make_parser()

    # turn off namespaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    #override the default ContextHandler
    Handler = NoteHandler()
    parser.setContentHandler( Handler )
    
    for i in range(1,len(sys.argv)):
        # pass in first argument as input file.
        if ".enex" in sys.argv[i]:
            current_file = sys.argv[i].replace(".enex", "/")
            try:
                parser.parse(sys.argv[i])
            except:
                print(sys.argv[i] + " was unable to be parsed correctly.")
