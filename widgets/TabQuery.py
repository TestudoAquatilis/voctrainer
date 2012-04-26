#coding=utf8

from gi.repository import Gtk

from .BorderBox import *

class TabQuery(BorderBox):
	"""
	Class containing widgets for querying.
	"""

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
		self.__inOut.setState('locked')
		self.__setState('query')

	def __solve(self):
		if len(self.__nextVoc.keys()) < 5:
			return
		self.__inOut.setData(self.__nextVoc)
		self.__inOut.setState('enabled')
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
		self.__inOut.setTypList(self.__db.getTypList())
	
	def __handlerDelete(self, widget, data=None):
		self.__db.deleteVoc(self.__nextVoc)
		self.__getNextVoc()
		self.__query()

	def __init__(self, db, inOut):
		"""
		Constructor.

		@param db database to interact with
		@param inOut VocInOut-widget to interact with
		"""

		BorderBox.__init__(self)

		self.__db    = db
		self.__inOut = inOut
		self.__state = 'query'

		self.addButton('Nächste',         self.__handlerNext)
		self.addSeparator()
		self.addButton('_Lösen',          self.__handlerSolve,    ['query'])
		self.addButton('_Gewusst',        self.__handlerKnown,    ['solution'])
		self.addButton('_Nicht gewusst',  self.__handlerNotKnown, ['solution'])
		self.addSeparator()
		self.addButton('Vokabel Ändern',  self.__handlerUpdate,   ['solution'])
		self.addButton('Vokabel Löschen', self.__handlerDelete,   ['solution'])

		self.setState('query')

		self.__nextVoc = db.getNext()
		
	def setActive(self):
		"""
		Call this function, if this Tab becomes active.
		"""

		self.__getNextVoc()

		if self.__state == 'solution':
			self.__solve()
		else:
			self.__query()
	
	def __setState(self, state):
		self.__state = state
		self.setState(state)
