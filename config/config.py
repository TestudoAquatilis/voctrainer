import pango

fonts = {
		'Medium': '20',
		'Kanji':  'IPAMincho 40'
	}

def getFont(id):
	desc = ''

	if id in fonts.keys():
		desc = fonts[id]
	
	return pango.FontDescription(desc)
