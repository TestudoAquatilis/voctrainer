#coding=utf8

import pygtk
import gtk

from BorderBox import *

class TabEdit:
	"""
	Class containing widgets for modifying vocabulary.
	"""

	def __handlerClear(self, widget, data=None):
		self.__inOut.clearData()
		self.__setState('new')

	def __handlerInsert(self, widget, data=None):
		entries = self.__inOut.getData()

		if len(entries['Deutsch']) == 0 or len(entries['Kana']) == 0:
			return

		if self.__db.hasVoc(entries):
			dialog = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, 'Vokabel existiert bereits!')
			dialog.run()
			dialog.destroy()
			return

		self.__db.addVoc(entries)
		self.__inOut.clearData()
		self.__inOut.setTypList(self.__db.getTypList())
		self.__setState('new')
	
	def __handlerSearch(self, widget, data=None):
		searchResults      = self.__db.searchVoc(self.__inOut.getData())
		self.__searchResults = searchResults
		comboBox           = self.__searchResultBox

		comboBox.get_model().clear()

		for i_result in searchResults:
			text = i_result['Deutsch'] + ' - ' + i_result['Kana']
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
			self.__inOut.setTypList(self.__db.getTypList())
	
	def __handlerDelete(self, widget, data=None):
		if not self.__currentVoc:
			return

		self.__db.deleteVoc(self.__currentVoc)

		index = self.__searchResultBox.get_active()
		self.__searchResults.pop(index)
		self.__searchResultBox.remove_text(index)
		if len(self.__searchResults) > 0:
			self.__searchResultBox.set_active(0)
		else:
			self.__searchResultBox.set_active(-1)

	def __init__(self, db, inOut):
		"""
		Constructor.

		@param db database to interact with
		@param inOut VocInOut-widget to interact with
		"""

		self.__db    = db
		self.__inOut = inOut
		self.__state = 'new'

		borderBox  = BorderBox()
		comboBox   = gtk.combo_box_new_text()

		comboBox.connect('changed', self.__handlerCBXResultChanged)

		borderBox.addButton('Eingabefelder leeren', self.__handlerClear)
		borderBox.addSeparator()
		borderBox.addButton('_Suchen',              self.__handlerSearch, ['new'])
		borderBox.addWidget(comboBox,                                   ['existing'])
		borderBox.addSeparator()
		borderBox.addButton('Vokabel _Einfügen',    self.__handlerInsert, ['new'])
		borderBox.addButton('Vokabel Ändern',       self.__handlerModify, ['existing'])
		borderBox.addButton('Vokabel Löschen',      self.__handlerDelete, ['existing'])

		comboBox.show()
		borderBox.setState('new')
		borderBox.show()
		
		self.__box             = borderBox
		self.__searchResultBox = comboBox
		self.__widget          = borderBox.getWidget()

		self.__currentVoc      = None
		self.__searchResults   = []

	def getWidget(self):
		"""
		Return the widget containing all widgets of this Tab

		@return gtk.Widget containing all widgets of this Tab
		"""

		return self.__widget

	def setActive(self):
		"""
		Call this function, if this Tab becomes active.
		"""

		self.__inOut.setSensitive(True)
		if self.__state == 'existing':
			self.__inOut.setData(self.__currentVoc)
		else:
			self.__inOut.clearData()

	def __setState(self, state):
		self.__state = state
		self.__box.setState(state)
