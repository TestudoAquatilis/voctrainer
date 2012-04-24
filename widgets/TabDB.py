#coding=utf8

import pygtk
import gtk

from BorderBox import *

class TabDB:
	def __handlerResetLevel(self, widget, data=None):
		self.db.resetLevel()
	
	def __handlerExportDB(self, widget, data=None):
		dialog  = gtk.FileChooserDialog('Exportiere DB in Datei', None, gtk.FILE_CHOOSER_ACTION_SAVE, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
		ffilter = gtk.FileFilter()
		ffilter.set_name('CSV-Datei')
		ffilter.add_pattern('*.csv')
		dialog.set_filter(ffilter)
		dialog.set_filename('vocabDB.csv')

		response = dialog.run()

		if response != gtk.RESPONSE_OK:
			dialog.destroy()
			return

		filename = dialog.get_filename()
		dialog.destroy()

		self.db.exportToFile(filename)
	
	def __handlerImportDB(self, widget, data=None):
		dialog  = gtk.FileChooserDialog('Exportiere DB in Datei', None, gtk.FILE_CHOOSER_ACTION_OPEN, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
		ffilter = gtk.FileFilter()
		ffilter.set_name('CSV-Datei')
		ffilter.add_pattern('*.csv')
		dialog.set_filter(ffilter)
		dialog.set_filename('vocabDB.csv')

		response = dialog.run()

		if response != gtk.RESPONSE_OK:
			dialog.destroy()
			return

		filename = dialog.get_filename()
		dialog.destroy()

		self.db.importFromFile(filename)

	def __init__(self, db, inOut):
		self.db    = db
		self.inOut = inOut

		borderBox  = BorderBox()

		borderBox.addButton('Fortschritt zurücksetzen', self.__handlerResetLevel)
		borderBox.addSeparator()
		borderBox.addButton('Datenbank exportieren',    self.__handlerExportDB)
		borderBox.addButton('Datenbank importieren',    self.__handlerImportDB)

		borderBox.show()

		self.widget = borderBox.getWidget()
	
	def getWidget(self):
		return self.widget

	def setActive(self):
		self.inOut.clearData()
		self.inOut.setSensitive(False)
