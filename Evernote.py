#/usr/bin/python

import xml.sax # Steaming XML data for use with larger files
import base64 # For converting base64 Evernote attachments
import os
import sys
import mimetypes # Converts mime file types into an extension
import time # Used to set the modified and access time of the file
import imp
try:
	imp.find_module('magic')
except ImportError:
	pip install filemagic
import magic # Needed to get the file extension because Evernotes caused errors


# Decode and Export base64 to file
def decodeBase64(encoded, fileName):
	try:
		rawdata = base64.b64decode(encoded)
	except TypeError, te:
		print 'TypeError: ', te
		raise SystemExit

	# Write the file out
	with file(fileName, 'wb') as outfile:
		outfile.write(rawdata)


class NoteHandler( xml.sax.ContentHandler ):
	def __init__(self):
		self.CurrentData = ""
		self.title = ""
		self.content = ""

	# New element found
	# Work with attributes such as: <en-media hash="kasd92">
	def startElement(self, tag, attributes):
		self.CurrentData = tag
		if tag == "title":
			self.dataCounter = 0
		elif tag == "en-media":
			hash = attributes["hash"]
		elif tag == "data":
			self.file = open('temp.enc', 'wa')
			print "Start data read."

	# When an element has finished reading this is called.
	# Process the collected data
	def endElement(self, tag):
		if self.CurrentData == "title":
			print "Title: ", self.title
		elif self.CurrentData == "data":
			self.file.close()
		elif self.CurrentData == "mime":

			# I tried directly converting from memory, but it was too slow.
			# Converting from a temp file sped up the process
			self.file = open('temp.enc', 'r')

			# Counter incase a note has multiple attachments
			self.dataCounter += 1

			if not os.path.exists('output')
				os.makedirs('output')
			fileName = 'output/' + self.created + str(self.dataCounter)
			decodeBase64(self.file.read(), fileName)
			self.file.close()	

			# Check the file for filetype and add the correct extension
			# I tried using Evernote's Mime-Types but some png files were marked as jpg
			mime = magic.from_file(fileName, mime=True)
			self.extension = mimetypes.guess_extension(mime)
			self.extension = self.extension.replace('.jpe', '.jpg')
			newFileName = fileName + self.extension
			os.rename(fileName, newFileName)

			# Set the date and time of the note to the file modified and access
			timeStamp = time.mktime(time.strptime(self.created, "%Y%m%dT%H%M%SZ"))
			os.utime(newFileName, (timeStamp, timeStamp))

			# Clean up temp files
			os.remove('temp.enc')

	def characters(self, content):
		if self.CurrentData == "title":
			self.title = content
		elif self.CurrentData == "created":
			self.created = content
		elif self.CurrentData == "data":
			# Remove linebreaks added in the enex file to prepare for decoding
			self.file.write(content.rstrip('\n'))

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
