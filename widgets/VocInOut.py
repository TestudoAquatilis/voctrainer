#coding=utf8

import pygtk
import gtk

import config

class VocInOut:
	"""
	Class holding the gtk.Widgets for input and output.

	Contains entries for the fields in the database and
	functions for easily setting and getting the values
	as dictionaries.

	All data dictionaries are of type:
	@code {
	'Deutsch': <value>,
	'Kana':    <value>,
	'Kanji':   <value>,
	'Typ':     <value>,
	'Info':    <value>}@endcode
	"""

	class entryInOut:
		"""
		Nested class for abstraction from gtk.Entry.
		"""

		def __init__(self, entry):
			"""
			Constructor.

			@param entry the @code gtk.Entry @endcode text is interchanged with
			"""
			self.entry = entry

		def getText(self):
			"""
			Returns the text of the Entry.

			@return The text of the Entry as string
			"""
			return self.entry.get_text().decode('utf-8')

		def setText(self, text):
			"""
			Sets the text of the Entry.

			@param text the text as string
			"""
			self.entry.set_text(text)

		def setSensitive(self, sensitivity):
			"""
			Sets the sensitivity of the Entry.

			@param sensitivity sensitivity as boolean
			"""
			self.entry.set_sensitive(sensitivity)
	
	class textViewInOut:
		"""
		Nested class for abstraction from gtk.TextView.
		"""
		def __init__(self, textView):
			"""
			Constructor.

			@param textView the @code gtk.TextView @endcode text is interchanged with
			"""
			self.textView = textView

		def getText(self):
			"""
			Returns the text of the TextView.

			@return The text of the TextView
			"""
			return self.textView.get_buffer().get_text(self.textView.get_buffer().get_start_iter(), self.textView.get_buffer().get_end_iter()).decode('utf-8')

		def setText(self, text):
			"""
			Sets the text of the TextView.

			@param text the text as string
			"""
			self.textView.get_buffer().set_text(text)

		def setSensitive(self, sensitivity):
			"""
			Sets the sensitivity of the TextView.

			@param sensitivity the sensitivity as boolean
			"""
			self.textView.set_sensitive(sensitivity)

	def __init__(self):
		table = gtk.Table(2, 5, False)

		fontKanji  = config.getFont('Kanji')
		fontMedium = config.getFont('Medium')

		entryDeutsch = gtk.Entry()
		entryKana    = gtk.Entry()
		entryKanji   = gtk.Entry()
		entryTyp     = gtk.Entry()
		entryInfo    = gtk.TextView()
		
		entryDeutsch.modify_font(fontMedium)
		entryKana.modify_font(fontMedium)
		entryKanji.modify_font(fontKanji)
		#entryTyp.modify_font(fontKanji)
		entryInfo.modify_font(fontMedium)

		labelDeutsch = gtk.Label('Deutsch:')
		labelKana    = gtk.Label('Kana:')
		labelKanji   = gtk.Label('Kanji:')
		labelTyp     = gtk.Label('Typ:')
		labelInfo    = gtk.Label('Info:')

		labelXOpt = 0
		labelYOpt = 0

		table.attach(labelDeutsch, 0, 1, 0, 1, labelXOpt, labelYOpt)
		table.attach(labelKana,    0, 1, 1, 2, labelXOpt, labelYOpt)
		table.attach(labelKanji,   0, 1, 2, 3, labelXOpt, labelYOpt)
		table.attach(labelTyp,     0, 1, 3, 4, labelXOpt, labelYOpt)
		table.attach(labelInfo,    0, 1, 4, 5, labelXOpt, labelYOpt)

		entryXOpt    = gtk.EXPAND|gtk.FILL
		entryYOpt    = gtk.FILL
		entryYOptExp = gtk.EXPAND|gtk.FILL

		table.attach(entryDeutsch, 1, 2, 0, 1, entryXOpt, entryYOpt)
		table.attach(entryKana,    1, 2, 1, 2, entryXOpt, entryYOpt)
		table.attach(entryKanji,   1, 2, 2, 3, entryXOpt, entryYOpt)
		table.attach(entryTyp,     1, 2, 3, 4, entryXOpt, entryYOpt)
		table.attach(entryInfo,    1, 2, 4, 5, entryXOpt, entryYOptExp)

		entryDeutsch.show()
		entryKana.show()
		entryKanji.show()
		entryTyp.show()
		entryInfo.show()

		labelDeutsch.show()
		labelKana.show()
		labelKanji.show()
		labelTyp.show()
		labelInfo.show()

		table.show()

		self.widget = table

		entries = {}
		entries['Deutsch'] = self.entryInOut(entryDeutsch)
		entries['Kana']    = self.entryInOut(entryKana)
		entries['Kanji']   = self.entryInOut(entryKanji)
		entries['Typ']     = self.entryInOut(entryTyp)
		entries['Info']    = self.textViewInOut(entryInfo)

		self.entries = entries

	def getWidget(self):
		"""
		Returns the outer container widget.

		@return the @code gtk.Widget @endcode containing all the needed widgets
		"""
		return self.widget

	def getData(self):
		"""
		Returns the data of the input fields as dictionary.

		@return the data of the input fields as dictionary
		"""
		result = {}

		for i_key in self.entries.keys():
			result[i_key] = self.entries[i_key].getText()

		return result
	
	def setData(self, data):
		"""
		Sets the data of the input fields.

		@param data the data as dictionary
		"""
		for i_key in self.entries.keys():
			if i_key in data.keys():
				self.entries[i_key].setText(data[i_key])
			else:
				self.entries[i_key].setText('')
	
	def clearData(self):
		"""
		Resets the data of the input fields
		"""
		for i_val in self.entries.values():
			i_val.setText('')
	
	def setSensitive(self, sensitivity):
		"""
		Sets sensitivity of input fields.

		@param sensitivity sensitivity as boolean
		"""
		for i_val in self.entries.values():
			i_val.setSensitive(sensitivity)
