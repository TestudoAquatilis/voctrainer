from gi.repository import Gtk

from .BorderBox import *

class TabQuery(BorderBox):
	"""
	Class containing widgets for querying.
	"""

	def __getNextVoc(self):
		oldAmount = self.__currentAmount
		oldVoc    = self.__nextVoc

		self.__nextVoc       = self.__db.getNext()
		self.__currentAmount = self.__db.getAmountOfCurrentVocab()

		if self.__currentAmount == 0:
			if oldAmount > 0:
				messageText = config.getDisplayString('TEDiaAmountZeroInfo')
				dialog = Gtk.MessageDialog(message_type=Gtk.MessageType.INFO, buttons=Gtk.ButtonsType.OK, message_format=messageText)

				response = dialog.run()
				dialog.destroy()

		if oldVoc != self.__nextVoc:
			self.__setState('query')
	
	def __query(self):
		if len(self.__nextVoc.keys()) < 5:
			return
		data = self.__nextVoc.copy()
		data['Lang2'] = ''
		data['Special'] = ''
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

	def __handlerModify(self, widget, data=None):
		entries = self.__inOut.getData()
		self.__db.modifyVoc(self.__nextVoc, entries)
		self.__inOut.setTypeList(self.__db.getTypeList())
	
	def __handlerDelete(self, widget, data=None):
		messageText = config.getDisplayString('TEDiaDeleteWarning')
		dialog = Gtk.MessageDialog(message_type=Gtk.MessageType.WARNING, buttons=Gtk.ButtonsType.YES_NO, message_format=messageText)

		response = dialog.run()
		dialog.destroy()

		if response != Gtk.ResponseType.YES:
			return

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

		self.addButton('TQueryNext',     self.__handlerNext)
		self.addSeparator()
		self.addButton('TQuerySolve',    self.__handlerSolve,    ['query'])
		self.addButton('TQueryKnown',    self.__handlerKnown,    ['solution'])
		self.addButton('TQueryNotKnown', self.__handlerNotKnown, ['solution'])
		self.addSeparator()
		self.addButton('TQueryModify',   self.__handlerModify,   ['solution'])
		self.addButton('TQueryDelete',   self.__handlerDelete,   ['solution'])

		self.setState('query')

		self.__nextVoc       = db.getNext()
		self.__currentAmount = db.getAmountOfCurrentVocab()
		
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
