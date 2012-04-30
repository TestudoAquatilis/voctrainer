#coding=utf8

from gi.repository import Gtk

from .BorderBox import *
import config

class TabDB(BorderBox):
	"""
	Class containing widgets for general database operations.
	"""

	def __handlerResetLevel(self, widget, data=None):
		self.__db.resetLevel()
	
	def __handlerStatistics(self, widget, data=None):
		statistics = self.__db.getStatistics()

		dialog = Gtk.Dialog('Test', buttons = (Gtk.STOCK_OK, Gtk.ResponseType.OK))

		table = Gtk.Table(2, len(statistics)+1, False)

		vocsum = 0
		
		for i_val in statistics.values():
			vocsum += i_val

		labelLeft  = Gtk.Label('Level:')
		labelRight = Gtk.Label('Fortschritt:')

		table.attach(labelLeft,  0, 1, 0, 1, xpadding=4, ypadding=4)
		table.attach(labelRight, 1, 2, 0, 1, xpadding=4, ypadding=4)

		separator = Gtk.Separator(orientation = Gtk.Orientation.HORIZONTAL)
		table.attach(separator, 0, 2, 1, 2)

		i = 2

		for i_key in statistics.keys():
			labelLeft   = Gtk.Label(i_key)
			progressbar = Gtk.ProgressBar()
			progressbar.set_text(str(statistics[i_key]))
			progressbar.set_show_text(True)
			progressbar.set_fraction(statistics[i_key]/vocsum)

			table.attach(labelLeft,   0, 1, i, i+1, xpadding=4, ypadding=4)
			#table.attach(labelRight, 1, 2, i, i+1)
			table.attach(progressbar, 1, 2, i, i+1, xpadding=4, ypadding=2)

			i      += 1

		separator = Gtk.Separator(orientation = Gtk.Orientation.HORIZONTAL)
		table.attach(separator, 0, 2, i, i+1)

		i += 1

		labelLeft  = Gtk.Label('Summe:')
		labelRight = Gtk.Label(vocsum)

		table.attach(labelLeft,  0, 1, i, i+1, xpadding=4, ypadding=4)
		table.attach(labelRight, 1, 2, i, i+1, xpadding=4, ypadding=4)

		table.show_all()

		dialog.get_content_area().add(table)

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

		self.addButton('TDBReset',      self.__handlerResetLevel)
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
