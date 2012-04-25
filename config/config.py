import pango

__fonts = {
		'Medium': '20',
		'Kanji':  'IPAMincho 40'
	}

__filenames = {
		'Database': 'vocabulary.db'
	}

def getFont(id):
	"""
	Get the font for the given id.

	@param id the id of the font as string
	@return the font as pango FontDescription
	"""

	desc = ''

	if id in __fonts.keys():
		desc = __fonts[id]
	
	return pango.FontDescription(desc)

def getFilename(id):
	"""
	Get the filename for the given id.

	@param id the id of the filename as string
	@return the filename as string
	"""

	result = None

	if id in __filenames.keys():
		result = __filenames[id]
	
	return result
