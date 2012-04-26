#coding=utf8

from gi.repository import Gtk

import config

class VocInOut(Gtk.Table):
	"""
	Class holding the Gtk.Widgets for input and output.

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

	class __entryInOut:
		"""
		Nested class for abstraction from Gtk.Entry.
		"""

		def __init__(self, entry):
			"""
			Constructor.

			@param entry the @code Gtk.Entry @endcode text is interchanged with
			"""

			self.__entry = entry

		def getText(self):
			"""
			Returns the text of the Entry.

			@return The text of the Entry as string
			"""

			return self.__entry.get_text() #.decode('utf-8')

		def setText(self, text):
			"""
			Sets the text of the Entry.

			@param text the text as string
			"""

			self.__entry.set_text(text)

		def setSensitive(self, sensitivity):
			"""
			Sets the sensitivity of the Entry.

			@param sensitivity sensitivity as boolean
			"""

			self.__entry.set_sensitive(sensitivity)
	
	class __comboBoxEntryInOut:
		"""
		Nested class for abstraction from Gtk.ComboBoxEntry.
		"""

		def __init__(self, cbxEntry):
			"""
			Constructor.

			@param cbxentry the @code Gtk.ComboBoxEntry @endcode text is interchanged with
			"""

			self.__cbxEntry = cbxEntry

		def getText(self):
			"""
			Returns the text of the ComboBoxEntry.

			@return the text of the ComboBoxEntry as string
			"""

			return self.__cbxEntry.get_child().get_text() #.decode('utf-8')

		def setText(self, text):
			"""
			Sets the text of the ComboBoxEntry

			@param text the text as string
			"""

			self.__cbxEntry.get_child().set_text(text)

		def setSensitive(self, sensitivity):
			"""
			Sets the sensitivity of the ComboBoxEntry.

			@param sensitivity sensitivity as boolean
			"""

			self.__cbxEntry.set_sensitive(sensitivity)


	class __textViewInOut:
		"""
		Nested class for abstraction from Gtk.TextView.
		"""

		def __init__(self, textView):
			"""
			Constructor.

			@param textView the @code Gtk.TextView @endcode text is interchanged with
			"""

			self.__textView = textView

		def getText(self):
			"""
			Returns the text of the TextView.

			@return The text of the TextView
			"""

			return self.__textView.get_buffer().get_text(self.__textView.get_buffer().get_start_iter(), self.__textView.get_buffer().get_end_iter(), False) #.decode('utf-8')

		def setText(self, text):
			"""
			Sets the text of the TextView.

			@param text the text as string
			"""

			self.__textView.get_buffer().set_text(text)

		def setSensitive(self, sensitivity):
			"""
			Sets the sensitivity of the TextView.

			@param sensitivity the sensitivity as boolean
			"""

			self.__textView.set_sensitive(sensitivity)

	def __init__(self):
		"""
		Constructor.
		"""

		Gtk.Table.__init__(self, 2, 5, False)

		fontKanji  = config.getFont('Kanji')
		fontMedium = config.getFont('Medium')

		entryDeutsch = Gtk.Entry()
		entryKana    = Gtk.Entry()
		entryKanji   = Gtk.Entry()
		#entryTyp     = Gtk.Entry()
		entryTyp     = Gtk.ComboBoxText.new_with_entry()
		entryInfo    = Gtk.TextView()
		
		entryDeutsch.modify_font(fontMedium)
		entryKana.modify_font(fontMedium)
		entryKanji.modify_font(fontKanji)
		#entryTyp.modify_font(fontKanji)
		entryInfo.modify_font(fontMedium)

		labelDeutsch = Gtk.Label('Deutsch:')
		labelKana    = Gtk.Label('Kana:')
		labelKanji   = Gtk.Label('Kanji:')
		labelTyp     = Gtk.Label('Typ:')
		labelInfo    = Gtk.Label('Info:')

		labelXOpt = 0
		labelYOpt = 0

		self.attach(labelDeutsch, 0, 1, 0, 1, labelXOpt, labelYOpt)
		self.attach(labelKana,    0, 1, 1, 2, labelXOpt, labelYOpt)
		self.attach(labelKanji,   0, 1, 2, 3, labelXOpt, labelYOpt)
		self.attach(labelTyp,     0, 1, 3, 4, labelXOpt, labelYOpt)
		self.attach(labelInfo,    0, 1, 4, 5, labelXOpt, labelYOpt)

		entryXOpt    = Gtk.AttachOptions.EXPAND|Gtk.AttachOptions.FILL
		entryYOpt    = Gtk.AttachOptions.FILL
		entryYOptExp = Gtk.AttachOptions.EXPAND|Gtk.AttachOptions.FILL

		self.attach(entryDeutsch, 1, 2, 0, 1, entryXOpt, entryYOpt)
		self.attach(entryKana,    1, 2, 1, 2, entryXOpt, entryYOpt)
		self.attach(entryKanji,   1, 2, 2, 3, entryXOpt, entryYOpt)
		self.attach(entryTyp,     1, 2, 3, 4, entryXOpt, entryYOpt)
		self.attach(entryInfo,    1, 2, 4, 5, entryXOpt, entryYOptExp)

		entries = {}
		entries['Deutsch'] = self.__entryInOut(entryDeutsch)
		entries['Kana']    = self.__entryInOut(entryKana)
		entries['Kanji']   = self.__entryInOut(entryKanji)
		#entries['Typ']     = self.__entryInOut(entryTyp)
		entries['Typ']     = self.__comboBoxEntryInOut(entryTyp)
		entries['Info']    = self.__textViewInOut(entryInfo)

		self.__entries = entries
		self.__cbxTyp  = entryTyp

	def setTypList(self, typList):
		"""
		Sets the 'Typ'-values to select from

		@param typList array of 'Typ'-values as strings
		"""

		cbx   = self.__cbxTyp
		model = cbx.get_model()

		model.clear()

		for i_typ in typList:
			cbx.append_text(i_typ)

	def getData(self):
		"""
		Returns the data of the input fields as dictionary.

		@return the data of the input fields as dictionary
		"""

		result = {}

		for i_key in self.__entries.keys():
			result[i_key] = self.__entries[i_key].getText()

		return result
	
	def setData(self, data):
		"""
		Sets the data of the input fields.

		@param data the data as dictionary
		"""

		for i_key in self.__entries.keys():
			if i_key in data.keys():
				self.__entries[i_key].setText(data[i_key])
			else:
				self.__entries[i_key].setText('')
	
	def clearData(self):
		"""
		Resets the data of the input fields
		"""

		for i_val in self.__entries.values():
			i_val.setText('')
	
	def setSensitive(self, sensitivity):
		"""
		Sets sensitivity of input fields.

		@param sensitivity sensitivity as boolean
		"""

		for i_val in self.__entries.values():
			i_val.setSensitive(sensitivity)
