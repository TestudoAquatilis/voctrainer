from gi.repository import Gtk

from .BorderBox import *
from .DialogStatistics import *
import config

class TabDB(BorderBox):
	"""
	Class containing widgets for general database operations.
	"""

	def __handlerShuffleCurrent(self, widget, data=None):
		amount = self.__db.shuffleCurrent()

		messageText = config.getDisplayString('TDBDiaShuffleInfo') % (amount,)
		dialog = Gtk.MessageDialog(message_type=Gtk.MessageType.INFO, buttons=Gtk.ButtonsType.OK, message_format=messageText)

		dialog.run()
		dialog.destroy()

	def __handlerResetLevel(self, widget, data=None):
		messageText = config.getDisplayString('TDBDiaResetWarning')
		dialog = Gtk.MessageDialog(message_type=Gtk.MessageType.WARNING, buttons=Gtk.ButtonsType.YES_NO, message_format=messageText)

		response = dialog.run()
		dialog.destroy()

		if response == Gtk.ResponseType.YES:
			self.__db.resetLevel()
	
	def __handlerStatistics(self, widget, data=None):
		dialog = DialogStatistics(self.__db)

		dialog.run()
		dialog.destroy()

	def __handlerExportDB(self, widget, data=None):
		dialog  = Gtk.FileChooserDialog(config.getDisplayString('TDBFCExport'), None, Gtk.FileChooserAction.SAVE, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_SAVE, Gtk.ResponseType.OK))
		ffilter = Gtk.FileFilter()
		ffilter.set_name(config.getDisplayString('TDBFFCSV'))
		ffilter.add_pattern('*.csv')
		dialog.set_filter(ffilter)
		dialog.set_filename('vocabDB.csv')

		response = dialog.run()

		if response != Gtk.ResponseType.OK:
			dialog.destroy()
			return

		filename = dialog.get_filename()
		dialog.destroy()

		self.__db.exportToFile(filename)
	
	def __handlerImportDB(self, widget, data=None):
		dialog  = Gtk.FileChooserDialog(config.getDisplayString('TDBFCImport'), None, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
		ffilter = Gtk.FileFilter()
		ffilter.set_name(config.getDisplayString('TDBFFCSV'))
		ffilter.add_pattern('*.csv')
		dialog.set_filter(ffilter)
		dialog.set_filename('vocabDB.csv')

		response = dialog.run()

		if response != Gtk.ResponseType.OK:
			dialog.destroy()
			return

		filename = dialog.get_filename()
		dialog.destroy()

		self.__db.importFromFile(filename)
		self.__inOut.setTypeList(self.__db.getTypeList())

	def __init__(self, db, inOut):
		"""
		Constructor.

		@param db database to interact with
		@param inOut VocInOut-widget to interact with
		"""

		BorderBox.__init__(self)

		self.__db    = db
		self.__inOut = inOut

		self.addButton('TDBShuffle',    self.__handlerShuffleCurrent)
		self.addButton('TDBReset',      self.__handlerResetLevel)
		self.addSeparator()
		self.addButton('TDBStatistics', self.__handlerStatistics)
		self.addSeparator()
		self.addButton('TDBExport',     self.__handlerExportDB)
		self.addButton('TDBImport',     self.__handlerImportDB)

	def setActive(self):
		"""
		Call this function, if this Tab becomes active.
		"""

		self.__inOut.clearData()
		self.__inOut.setState('disabled')
