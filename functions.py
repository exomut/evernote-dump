import base64 # For converting base64 Evernote attachments
import os
import sys
from language import *

def checkForDouble(path):
	'''
	# Check file path and modifies it if a duplicate is found.
	# Used for creating new files.
	# Works with file extensions too.
			
	path: to desired save point
	
	returns: an updated path if path double found
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

def decodeBase64(encoded, fileName):
	'''
	# Decode and Export base64 to file

	encoded: raw encoded data
	filename: name of file to export to

	return: none
	'''

	try:
		rawdata = base64.b64decode(encoded)
	except TypeError:
		print('TypeError: ')
		raise SystemExit

	# Write the file out
	with file('temp/' + fileName, 'wb') as outfile:
		outfile.write(rawdata)

def isYesNo(phrase):
	'''
	# Ask as yes/no question and have the input check and turned into
	# a boolean. Compatible with all versions of Python.

	phrase: Yes/No phrase you would like to get input from user for

	returns: True for yes, False for no
	'''

	while True:
		if sys.version_info[:2] <= (2, 7):
			result = str(raw_input(lang(phrase) + '[y/n] '))
		else:
			result = str(input(lang(phrase) + '[y/n] '))

		if result.lower() == 'yes' or result.lower() == 'y':
			return True
		elif result.lower() == 'no' or result.lower() == 'n':
			return False
		print(lang('Please answer with "y" or "n" only.'))

def makeDirCheck(path):
	'''
	# Check if path exists. If not found path is created
	# and the path is returned.  

	path: location of new directory
	
	returns: path
	'''
	if not os.path.exists(path):
		os.makedirs(path)

	return path
