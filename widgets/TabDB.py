#coding=utf8

from gi.repository import Gtk

from .BorderBox import *

class TabDB(BorderBox):
	"""
	Class containing widgets for general database operations.
	"""

	def __handlerResetLevel(self, widget, data=None):
		self.__db.resetLevel()
	
	def __handlerExportDB(self, widget, data=None):
		dialog  = Gtk.FileChooserDialog('Exportiere DB in Datei', None, Gtk.FILE_CHOOSER_ACTION_SAVE, (Gtk.STOCK_CANCEL, Gtk.RESPONSE_CANCEL, Gtk.STOCK_OPEN, Gtk.RESPONSE_OK))
		ffilter = Gtk.FileFilter()
		ffilter.set_name('CSV-Datei')
		ffilter.add_pattern('*.csv')
		dialog.set_filter(ffilter)
		dialog.set_filename('vocabDB.csv')

		response = dialog.run()

		if response != Gtk.RESPONSE_OK:
			dialog.destroy()
			return

		filename = dialog.get_filename()
		dialog.destroy()

		self.__db.exportToFile(filename)
	
	def __handlerImportDB(self, widget, data=None):
		dialog  = Gtk.FileChooserDialog('Exportiere DB in Datei', None, Gtk.FILE_CHOOSER_ACTION_OPEN, (Gtk.STOCK_CANCEL, Gtk.RESPONSE_CANCEL, Gtk.STOCK_OPEN, Gtk.RESPONSE_OK))
		ffilter = Gtk.FileFilter()
		ffilter.set_name('CSV-Datei')
		ffilter.add_pattern('*.csv')
		dialog.set_filter(ffilter)
		dialog.set_filename('vocabDB.csv')

		response = dialog.run()

		if response != Gtk.RESPONSE_OK:
			dialog.destroy()
			return

		filename = dialog.get_filename()
		dialog.destroy()

		self.__db.importFromFile(filename)
		self.__inOut.setTypList(self.__db.getTypList())

	def __init__(self, db, inOut):
		"""
		Constructor.

		@param db database to interact with
		@param inOut VocInOut-widget to interact with
		"""

		BorderBox.__init__(self)

		self.__db    = db
		self.__inOut = inOut

		self.addButton('Fortschritt zurücksetzen', self.__handlerResetLevel)
		self.addSeparator()
		self.addButton('Datenbank exportieren',    self.__handlerExportDB)
		self.addButton('Datenbank importieren',    self.__handlerImportDB)

	def setActive(self):
		"""
		Call this function, if this Tab becomes active.
		"""

		self.__inOut.clearData()
		self.__inOut.setSensitive(False)
