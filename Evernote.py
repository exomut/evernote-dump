#/usr/bin/python
keepFileNames = False # Change this to true if you want original file names

import xml.sax # Steaming XML data for use with larger files
import os
import sys
import mimetypes # Converts mime file types into an extension
import time # Used to set the modified and access time of the file
import imp
from fileManager import *

try:
	import magic
except ImportError:
	print('\nError: Module filemagic required.')
	print('https://pypi.python.org/pypi/filemagic')
	print('Run: pip install filemagic\n')
	sys.exit(1)
	
# Functions
def makeDirCheck(path):
	'''
	path: location of new directory
	
	returns: True if directory was created, False if directory was found
	'''
	if not os.path.exists(path):
		os.makedirs(path)
		return True
	return False

def checkForDouble(path):
	'''
	path: to desired save point
	
	returns: a updated path if path double found
	'''
	doubleCounter = 2
	tempFileName = path 
	while os.path.exists(tempFileName):
		if len(path.rsplit('.',1)) > 1:
			tempFileName = path.rsplit('.', 1)[0] + \
						  '-' + str(doubleCounter) + '.' + \
						  path.rsplit('.', 1)[1]
		else:
			tempFileName += '-' + str(doubleCounter)
		doubleCounter += 1
	return tempFileName

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
		self.CurrentData = tag
		if tag == "title":
			self.dataCounter = 0
		elif tag == "en-media":
			hash = attributes["hash"]
		elif tag == "data":
			makeDirCheck('temp')
			self.file = open('temp/temp.enc', 'wa')

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

			makeDirCheck('output')
			fileName = self.created
			decodeBase64(self.file.read(), fileName)
			self.file.close()	
			newFileName = ''
			if self.filename and keepFileNames:
				newFileName = 'output/' + self.filename	
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

	# create an XMLReader
	parser = xml.sax.make_parser()
	# turn off namespaces
	parser.setFeature(xml.sax.handler.feature_namespaces, 0)

	#override the default ContextHandler
	Handler = NoteHandler()
	parser.setContentHandler( Handler )
	
	# pass in first argument as input file.
	parser.parse(sys.argv[1])
