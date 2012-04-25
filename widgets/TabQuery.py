#coding=utf8

import pygtk
import gtk

from BorderBox import *

class TabQuery:
	def __getNextVoc(self):
		oldVoc = self.__nextVoc

		self.__nextVoc = self.__db.getNext()

		if oldVoc != self.__nextVoc:
			self.__setState('query')
	
	def __query(self):
		if len(self.__nextVoc.keys()) < 5:
			return
		data = self.__nextVoc.copy()
		data['Kana'] = ''
		data['Kanji'] = ''
		data['Info'] = ''
		self.__inOut.setData(data)
		self.__setState('query')

	def __solve(self):
		if len(self.__nextVoc.keys()) < 5:
			return
		self.__inOut.setData(self.__nextVoc)
		self.__setState('solution')

	def __known(self):
		if len(self.__nextVoc.keys()) < 6:
			return
		self.__db.updateLevel(self.__nextVoc, self.__nextVoc['Level']+1)

	def __notKnown(self):
		if len(self.__nextVoc.keys()) < 6:
			return
		self.__db.updateLevel(self.__nextVoc, 0)

	def __handlerNext(self, widget, data=None):
		self.__getNextVoc()
		self.__query()

	def __handlerSolve(self, widget, data=None):
		self.__solve()

	def __handlerKnown(self, widget, data=None):
		self.__known()
		self.__getNextVoc()
		self.__query()
	
	def __handlerNotKnown(self, widget, data=None):
		self.__notKnown()
		self.__getNextVoc()
		self.__query()

	def __handlerUpdate(self, widget, data=None):
		entries = self.__inOut.getData()
		self.__db.modifyVoc(self.__nextVoc, entries)
	
	def __handlerDelete(self, widget, data=None):
		self.__db.deleteVoc(self.__nextVoc)
		self.__getNextVoc()
		self.__query()

	def __init__(self, db, inOut):
		self.__db    = db
		self.__inOut = inOut
		self.__state = 'query'

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

		self.__box     = borderBox

		self.__widget  = borderBox.getWidget()

		self.__nextVoc = db.getNext()
		
	def getWidget(self):
		return self.__widget

	def setActive(self):
		self.__inOut.setSensitive(True)
		self.__getNextVoc()

		if self.__state == 'solution':
			self.__solve()
		else:
			self.__query()
	
	def __setState(self, state):
		self.__state = state
		self.__box.setState(state)
