#!/usr/bin/env python
# -*- coding: utf-8 -*-

keepFileNames = False

import xml.sax # Steaming XML data for use with larger files
import os
import sys
import mimetypes # Converts mime file types into an extension
import time # Used to set the modified and access time of the file
import imp
import magic
import html2text # Convert html notes to markdown
from functions import *

class NoteHandler( xml.sax.ContentHandler ):
	def __init__(self):
		try:
			self.magic = magic.Magic(flags=magic.MAGIC_MIME_TYPE)
		except AttributeError:
			self.magic = magic.Magic(mime=True)
		self.CurrentData = ""
		self.title = ""
		self.note = ""
		self.content = ""
		self.filename = ""
		self.timestamp = ""
		self.html2text = html2text.HTML2Text()

	# New element found
	# Work with attributes such as: <en-media hash="kasd92">
	def startElement(self, tag, attributes):
		'''
		Called when a new element is found
		'''
		self.CurrentData = tag
		if tag == "title":
			self.dataCounter = 0
		elif tag == "content":
			self.note == ""
		elif tag == "en-media":
			hash = attributes["hash"]
		elif tag == "data":
			self.file = open(makeDirCheck('temp') + '/temp.enc', 'wa')

	# When an element has finished reading this is called.
	# Process the collected data
	def endElement(self, tag):
		if self.CurrentData == "title":
			print("Title: ", self.title)
		elif self.CurrentData == "content":
			with file(makeDirCheck('notes')+ '/' + self.title + '.md', 'wb') as outfile:
				result = self.html2text.handle(self.note.decode('utf8'))
				outfile.write(result.encode('utf-8'))
				outfile.close()

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
				mime = None
				try:
					mime = self.magic.id_filename('temp/' + fileName)
				except AttributeError:
					mime = self.magic.from_file('temp/' + fileName)

				self.extension = mimetypes.guess_extension(mime)
				self.extension = self.extension.replace('.jpe', '.jpg')
				newFileName = makeDirCheck('output/') + fileName + self.extension

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
