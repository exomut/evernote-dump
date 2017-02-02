#!/usr/bin/env python
# -*- coding: utf-8 -*-

keepFileNames = False # Change this to true if you want original file names

import xml.sax # Steaming XML data for use with larger files
import os
import sys
import mimetypes # Converts mime file types into an extension
import time # Used to set the modified and access time of the file
import imp
from functions import *
import magic

class NoteHandler( xml.sax.ContentHandler ):
	def __init__(self):
		self.CurrentData = ""
		self.title = ""
		self.content = ""
		self.filename = ""
		self.timestamp = ""

	# New element found
	# Work with attributes such as: <en-media hash="kasd92">
	def startElement(self, tag, attributes):
		'''
		Called when a new element is found
		'''
		self.CurrentData = tag
		if tag == "title":
			self.dataCounter = 0
		elif tag == "en-media":
			hash = attributes["hash"]
		elif tag == "data":
			self.file = open(makeDirCheck('temp') + '/temp.enc', 'wa')

	# When an element has finished reading this is called.
	# Process the collected data
	def endElement(self, tag):
		if self.CurrentData == "title":
			print("Title: ", self.title)
		elif self.CurrentData == "data":
			self.file.close()
		if tag == "resource":
			# I tried directly converting from memory, but it was too slow.
			# Converting from a temp file sped up the process
			self.file = open('temp/temp.enc', 'r')

			fileName = self.created
			decodeBase64(self.file.read(), fileName)
			self.file.close()	
			newFileName = ''
			if self.filename and keepFileNames:
				newFileName = makeDirCheck('output') + '/' + self.filename	
			else:
				# Check the file for filetype and add the correct extension
				# I tried using Evernote's Mime-Types but some png files were marked as jpg
				print(fileName)
				mime = magic.from_file('temp/' + fileName, mime=True)
				self.extension = mimetypes.guess_extension(mime)
				self.extension = self.extension.replace('.jpe', '.jpg')
				newFileName = 'output/' + fileName + self.extension

			newFileName = checkForDouble(newFileName)	
			os.rename('temp/' + fileName, newFileName)

			# Set the date and time of the note to the file modified and access
			timeStamp = time.mktime(time.strptime(self.created, "%Y%m%dT%H%M%SZ"))
			os.utime(newFileName, (timeStamp, timeStamp))

			# Clean up temp files
			os.remove('temp/temp.enc')
			self.timestamp == ""
			self.filename == ""

	def characters(self, content):
		if self.CurrentData == "title":
			self.title = content
		elif self.CurrentData == "created":
			self.created = content
		elif self.CurrentData == "data":
			# Remove linebreaks added in the enex file to prepare for decoding
			self.file.write(content.rstrip('\n'))
		elif self.CurrentData == "timestamp":
			self.timestamp = content
		elif self.CurrentData == "file-name":
			self.filename = content
			print(self.filename)


if ( __name__ == "__main__"):
	
	chooseLanguage()
	keepFileNames = isYesNo('Would you like to keep the original filenames' +
					' if found?')

	# create an XMLReader
	parser = xml.sax.make_parser()
	# turn off namespaces
	parser.setFeature(xml.sax.handler.feature_namespaces, 0)

	#override the default ContextHandler
	Handler = NoteHandler()
	parser.setContentHandler( Handler )
	
	# pass in first argument as input file.
	parser.parse(sys.argv[1])
