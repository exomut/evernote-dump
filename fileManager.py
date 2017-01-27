import base64 # For converting base64 Evernote attachments

# Decode and Export base64 to file
def decodeBase64(encoded, fileName):
	try:
		rawdata = base64.b64decode(encoded)
	except TypeError:
		print('TypeError: ')
		raise SystemExit

	# Write the file out
	with file('temp/' + fileName, 'wb') as outfile:
		outfile.write(rawdata)
