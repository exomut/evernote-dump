import base64 # For converting base64 Evernote attachments
import os

# Decode and Export base64 to file
def decodeBase64(encoded, fileName):
	'''
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

def makeDirCheck(path):
	'''
	path: location of new directory
	
	returns: path
	'''
	if not os.path.exists(path):
		os.makedirs(path)

	return path

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
