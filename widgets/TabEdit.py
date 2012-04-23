#coding=utf8

import pygtk
import gtk

from BorderBox import *

class TabEdit:
	def handlerClear(self, widget, data=None):
		self.inOut.clearData()
		self.setState('new')

	def handlerInsert(self, widget, data=None):
		entries = self.inOut.getData()

		if len(entries['Deutsch']) == 0 or len(entries['Kana']) == 0:
			return

		self.db.addVoc(entries)
		self.inOut.clearData()
		self.setState('new')
	
	def handlerSearch(self, widget, data=None):
		searchResults      = self.db.searchVoc(self.inOut.getData())
		self.searchResults = searchResults
		comboBox           = self.searchResultBox

		comboBox.get_model().clear()

		for i_result in searchResults:
			text = i_result['Deutsch'] + ' - ' + i_result['Kana']
			comboBox.append_text(text)

		if len(searchResults) > 0:
			comboBox.set_active(0)
		else:
			comboBox.set_active(-1)

	
	def handlerCBXResultChanged(self, widget, data=None):
		index = widget.get_active()

		if index < 0:
			self.currentVoc = None
			self.inOut.clearData()
			self.setState('new')
		else:
			self.currentVoc = self.searchResults[index]
			self.inOut.setData(self.currentVoc)
			self.setState('existing')
	
	def handlerModify(self, widget, data=None):
		if self.currentVoc:
			entries = self.inOut.getData()
			self.db.modifyVoc(self.currentVoc, entries)
	
	def handlerDelete(self, widget, data=None):
		if not self.currentVoc:
			return

		self.db.deleteVoc(self.currentVoc)

		index = self.searchResultBox.get_active()
		self.searchResults.pop(index)
		self.searchResultBox.remove_text(index)
		if len(self.searchResults) > 0:
			self.searchResultBox.set_active(0)
		else:
			self.searchResultBox.set_active(-1)

	def __init__(self, db, inOut):
		self.db    = db
		self.inOut = inOut
		self.state = 'new'

		borderBox  = BorderBox()
		comboBox   = gtk.combo_box_new_text()

		comboBox.connect('changed', self.handlerCBXResultChanged)

		borderBox.addButton('Eingabefelder leeren', self.handlerClear)
		borderBox.addSeparator()
		borderBox.addButton('Suchen',               self.handlerSearch, ['new'])
		borderBox.addWidget(comboBox,                                   ['existing'])
		borderBox.addSeparator()
		borderBox.addButton('Vokabel Einfügen',     self.handlerInsert, ['new'])
		borderBox.addButton('Vokabel Ändern',       self.handlerModify, ['existing'])
		borderBox.addButton('Vokabel Löschen',      self.handlerDelete, ['existing'])

		comboBox.show()
		borderBox.setState('new')
		borderBox.show()
		
		self.box             = borderBox
		self.searchResultBox = comboBox
		self.widget          = borderBox.getWidget()

		self.currentVoc      = None
		self.searchResults   = []

	def getWidget(self):
		return self.widget

	def setActive(self):
		self.inOut.setSensitive(True)
		if self.state == 'existing':
			self.inOut.setData(self.currentVoc)
		else:
			self.inOut.clearData()

	def setState(self, state):
		self.state = state
		self.box.setState(state)
