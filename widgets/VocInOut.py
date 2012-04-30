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
	'Lang1':   <value>,
	'Lang2':   <value>,
	'Special': <value>,
	'Type':    <value>,
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

			return self.__entry.get_text()

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

		def setEditable(self, editability):
			"""
			Sets the editability of the Entry.

			@param editability editability as boolean
			"""

			self.__entry.set_editable(editability)

		def setFocus(self):
			"""
			Sets the focus to this Widget.
			"""
			self.__entry.grab_focus()
	
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

			return self.__cbxEntry.get_child().get_text()

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

		def setEditable(self, editability):
			"""
			Sets the editability of the ComboBoxEntry.

			@param editability editability as boolean
			"""

			self.__cbxEntry.get_child().set_editable(editability)

		def setFocus(self):
			"""
			Sets the focus to this Widget.
			"""
			self.__cbxEntry.grab_focus()

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

			return self.__textView.get_buffer().get_text(self.__textView.get_buffer().get_start_iter(), self.__textView.get_buffer().get_end_iter(), False)

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

		def setEditable(self, editability):
			"""
			Sets the editability of the TextView.

			@param editability editability as boolean
			"""

			self.__textView.set_editable(editability)
			self.__textView.set_cursor_visible(editability)

		def setFocus(self):
			"""
			Sets the focus to this Widget.
			"""
			self.__textView.grab_focus()

	def __init__(self, dbMapping):
		"""
		Constructor.
		"""

		Gtk.Table.__init__(self, 2, 5, False)

		fontLang1   = config.getFont([dbMapping['Lang1'],   'Medium'])
		fontLang2   = config.getFont([dbMapping['Lang2'],   'Medium'])
		fontSpecial = config.getFont([dbMapping['Special'], 'Medium'])
		fontMedium  = config.getFont('Medium')

		entryLang1   = Gtk.Entry()
		entryLang2   = Gtk.Entry()
		entrySpecial = Gtk.Entry()
		entryType    = Gtk.ComboBoxText.new_with_entry()
		entryInfo    = Gtk.TextView()
		
		entryLang1.modify_font(fontLang1)
		entryLang2.modify_font(fontLang2)
		entrySpecial.modify_font(fontSpecial)
		#entryType.modify_font(fontSpecial)
		entryInfo.modify_font(fontMedium)

		listLabels   = ['Lang1', 'Lang2', 'Special', 'Type', 'Info']

		for i in range(0, 5):
			lCaption = dbMapping[listLabels[i]] + ':'
			label    = Gtk.Label(lCaption)

			label.set_justify(Gtk.Justification.LEFT)
			label.set_alignment(0, 0.5)

			labelXOpt = Gtk.AttachOptions.FILL
			labelYOpt = Gtk.AttachOptions.FILL

			self.attach(label, 0, 1, i, i+1, labelXOpt, labelYOpt, 4, 0)

		entryXOpt    = Gtk.AttachOptions.EXPAND|Gtk.AttachOptions.FILL
		entryYOpt    = Gtk.AttachOptions.FILL
		entryYOptExp = Gtk.AttachOptions.EXPAND|Gtk.AttachOptions.FILL

		self.attach(entryLang1,   1, 2, 0, 1, entryXOpt, entryYOpt)
		self.attach(entryLang2,   1, 2, 1, 2, entryXOpt, entryYOpt)
		self.attach(entrySpecial, 1, 2, 2, 3, entryXOpt, entryYOpt)
		self.attach(entryType,    1, 2, 3, 4, entryXOpt, entryYOpt)
		self.attach(entryInfo,    1, 2, 4, 5, entryXOpt, entryYOptExp)

		entries = {}
		entries['Lang1']   = self.__entryInOut(entryLang1)
		entries['Lang2']   = self.__entryInOut(entryLang2)
		entries['Special'] = self.__entryInOut(entrySpecial)
		entries['Type']    = self.__comboBoxEntryInOut(entryType)
		entries['Info']    = self.__textViewInOut(entryInfo)

		self.__entries = entries
		self.__cbxType = entryType

	def setTypeList(self, typList):
		"""
		Sets the 'Type'-values to select from

		@param typList array of 'Type'-values as strings
		"""

		cbx   = self.__cbxType
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
	
	def setFocus(self, entry):
		"""
		Sets the focus to the entry with the given name.

		@param entry the entry name
		"""

		if entry in self.__entries.keys():
			self.__entries[entry].setFocus()
	
	def setState(self, state):
		"""
		Sets the input field state.

		@param state one of 'enabled', 'locked', 'disabled'
		"""

		if state == 'enabled':
			editable  = True
			sensitive = True
		elif state == 'locked':
			editable  = False
			sensitive = True
		else:
			editable  = False
			sensitive = False

		for i_val in self.__entries.values():
			i_val.setSensitive(sensitive)
			i_val.setEditable (editable)
