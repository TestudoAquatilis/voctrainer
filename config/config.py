import pango

fonts = {
		'Medium': '20',
		'Kanji':  'IPAMincho 40'
	}

filenames = {
		'Database': 'vocabulary.db'
	}

def getFont(id):
	desc = ''

	if id in fonts.keys():
		desc = fonts[id]
	
	return pango.FontDescription(desc)

def getFilename(id):
	result = None

	if id in filenames.keys():
		result = filenames[id]
	
	return result
