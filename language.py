translation = {
		'Please answer with "y" or "n" only.':'Please answer with "y" or "n" only.',
		'Would you like to keep the original filenames if found?':'Would you like to keep the original filenames if found?'
}

def lang(phrase):
		if phrase in translation:
			return translation[phrase]
		else:
			return 'needs_translation entry'
