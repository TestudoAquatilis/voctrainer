#coding=utf8

import pygtk
import gtk

from BorderBox import *

class TabQuery:
	def getNextVoc(self):
		oldVoc = self.nextVoc

		self.nextVoc = self.db.getNext()

		if oldVoc != self.nextVoc:
			self.setState('query')
	
	def query(self):
		if len(self.nextVoc.keys()) < 5:
			return
		data = self.nextVoc.copy()
		data['Kana'] = ''
		data['Kanji'] = ''
		data['Info'] = ''
		self.inOut.setData(data)
		self.setState('query')

	def solve(self):
		if len(self.nextVoc.keys()) < 5:
			return
		self.inOut.setData(self.nextVoc)
		self.setState('solution')

	def known(self):
		if len(self.nextVoc.keys()) < 6:
			return
		self.db.updateLevel(self.nextVoc, self.nextVoc['Level']+1)

	def notKnown(self):
		if len(self.nextVoc.keys()) < 6:
			return
		self.db.updateLevel(self.nextVoc, 0)

	def __handlerNext(self, widget, data=None):
		self.getNextVoc()
		self.query()

	def __handlerSolve(self, widget, data=None):
		self.solve()

	def __handlerKnown(self, widget, data=None):
		self.known()
		self.getNextVoc()
		self.query()
	
	def __handlerNotKnown(self, widget, data=None):
		self.notKnown()
		self.getNextVoc()
		self.query()

	def __handlerUpdate(self, widget, data=None):
		entries = self.inOut.getData()
		self.db.modifyVoc(self.nextVoc, entries)
	
	def __handlerDelete(self, widget, data=None):
		self.db.deleteVoc(self.nextVoc)
		self.getNextVoc()
		self.query()

	def __init__(self, db, inOut):
		self.db    = db
		self.inOut = inOut
		self.state = 'query'

		borderBox  = BorderBox()

		borderBox.addButton('Nächste',         self.__handlerNext)
		borderBox.addSeparator()
		borderBox.addButton('_Lösen',          self.__handlerSolve,    ['query'])
		borderBox.addButton('_Gewusst',        self.__handlerKnown,    ['solution'])
		borderBox.addButton('_Nicht gewusst',  self.__handlerNotKnown, ['solution'])
		borderBox.addSeparator()
		borderBox.addButton('Vokabel Ändern',  self.__handlerUpdate,   ['solution'])
		borderBox.addButton('Vokabel Löschen', self.__handlerDelete,   ['solution'])

		borderBox.setState('query')
		borderBox.show()

		self.box     = borderBox

		self.widget  = borderBox.getWidget()

		self.nextVoc = db.getNext()
		
	def getWidget(self):
		return self.widget

	def setActive(self):
		self.inOut.setSensitive(True)
		self.getNextVoc()

		if self.state == 'solution':
			self.solve()
		else:
			self.query()
	
	def setState(self, state):
		self.state = state
		self.box.setState(state)
