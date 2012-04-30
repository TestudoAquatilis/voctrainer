from gi.repository import Gtk

from .BorderBox import *

class TabEdit(BorderBox):
	"""
	Class containing widgets for modifying vocabulary.
	"""

	def __handlerClear(self, widget, data=None):
		self.__inOut.clearData()
		self.__inOut.setFocus('Lang1')
		self.__setState('new')

	def __handlerInsert(self, widget, data=None):
		entries = self.__inOut.getData()

		if len(entries['Lang1']) == 0 or len(entries['Lang2']) == 0:
			return

		if self.__db.hasVoc(entries):
			dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, 'Vokabel existiert bereits!')
			dialog.run()
			dialog.destroy()
			return

		self.__db.addVoc(entries)
		self.__inOut.clearData()
		self.__inOut.setFocus('Lang1')
		self.__inOut.setTypeList(self.__db.getTypeList())
		self.__setState('new')
	
	def __trimResult(self, string):
		"""
		Trims string to 10 characters

		@param string the string to trim
		@return trimmed string
		"""

		if len(string) > 11:
			return string[0:10] + '...'
		else:
			return string

	def __handlerSearch(self, widget, data=None):
		searchResults      = self.__db.searchVoc(self.__inOut.getData())
		self.__searchResults = searchResults
		comboBox           = self.__searchResultBox

		comboBox.get_model().clear()

		for i_result in searchResults:
			
			text = self.__trimResult(i_result['Lang1']) + ' - ' + self.__trimResult(i_result['Lang2'])
			comboBox.append_text(text)

		if len(searchResults) > 0:
			comboBox.set_active(0)
		else:
			comboBox.set_active(-1)

	
	def __handlerCBXResultChanged(self, widget, data=None):
		index = widget.get_active()

		if index < 0:
			self.__currentVoc = None
			self.__inOut.clearData()
			self.__setState('new')
		else:
			self.__currentVoc = self.__searchResults[index]
			self.__inOut.setData(self.__currentVoc)
			self.__setState('existing')
	
	def __handlerModify(self, widget, data=None):
		if self.__currentVoc:
			entries = self.__inOut.getData()
			self.__db.modifyVoc(self.__currentVoc, entries)
			self.__inOut.setTypeList(self.__db.getTypeList())
	
	def __handlerDelete(self, widget, data=None):
		searchResults = self.__searchResults
		comboBox      = self.__searchResultBox

		if not self.__currentVoc:
			return

		messageText = config.getDisplayString('TEDiaDeleteWarning')
		dialog = Gtk.MessageDialog(message_type=Gtk.MessageType.WARNING, buttons=Gtk.ButtonsType.YES_NO, message_format=messageText)

		response = dialog.run()
		dialog.destroy()

		if response != Gtk.ResponseType.YES:
			return

		self.__db.deleteVoc(self.__currentVoc)

		index = comboBox.get_active()
		searchResults.pop(index)

		comboBox.get_model().clear()

		for i_result in searchResults:
			text = i_result['Lang1'] + ' - ' + i_result['Lang2']
			comboBox.append_text(text)

		if len(searchResults) > 0:
			comboBox.set_active(0)
		else:
			comboBox.set_active(-1)

	def __init__(self, db, inOut):
		"""
		Constructor.

		@param db database to interact with
		@param inOut VocInOut-widget to interact with
		"""

		BorderBox.__init__(self)

		self.__db    = db
		self.__inOut = inOut
		self.__state = 'new'

		comboBox   = Gtk.ComboBoxText()

		comboBox.connect('changed', self.__handlerCBXResultChanged)

		self.addButton('TEditClear',  self.__handlerClear)
		self.addSeparator()
		self.addButton('TEditSearch', self.__handlerSearch, ['new'])
		self.addWidget(comboBox,                            ['existing'], 'TEditSearchResults')
		self.addSeparator()
		self.addButton('TEditInsert', self.__handlerInsert, ['new'])
		self.addButton('TEditModify', self.__handlerModify, ['existing'])
		self.addButton('TEditDelete', self.__handlerDelete, ['existing'])

		self.setState('new')
		
		self.__searchResultBox = comboBox

		self.__currentVoc      = None
		self.__searchResults   = []

	def setActive(self):
		"""
		Call this function, if this Tab becomes active.
		"""

		self.__inOut.setState('enabled')

		if self.__state == 'existing':
			self.__inOut.setData(self.__currentVoc)
		else:
			self.__inOut.clearData()
			self.__inOut.setFocus('Lang1')

	def __setState(self, state):
		self.__state = state
		self.setState(state)
