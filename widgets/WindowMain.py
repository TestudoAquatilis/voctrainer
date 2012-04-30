#coding=utf8

from gi.repository import Gtk

from .VocInOut import *
from .TabEdit import *
from .TabQuery import *
from .TabDB import *

import config

class WindowMain(Gtk.Window):
	"""
	Main Window of the Program.

	Here the widgets are put in
	"""

	def __handlerDestroy(self, widget, data=None):
		Gtk.main_quit()
		self.__db.close()

	def __handlerPageChanged(self, widget, page, page_num, data=None):
		self.__pages[page_num].setActive()

	def __init__(self, db):
		"""
		Constructor.

		@param db The object, data is handled in as database.DBVoc
		@see database.DBVoc.DBVoc
		"""

		titleWindow = config.getDisplayString('WindowMainTitle')
		titleQuery  = config.getDisplayString('TabQueryTitle')
		titleEdit   = config.getDisplayString('TabEditTitle')
		titleDB     = config.getDisplayString('TabDBTitle')


		Gtk.Window.__init__(self, title = titleWindow)

		db        = db
		self.__db = db
		vocInOut  = VocInOut(db.getColumnMapping())

		vocInOut.setTypeList(db.getTypeList())

		boxOuter = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		notebook = Gtk.Notebook()

		tabQuery = TabQuery(db, vocInOut)
		tabEdit  = TabEdit (db, vocInOut)
		tabDB    = TabDB   (db, vocInOut)

		pages = {}

		page1 = notebook.append_page(tabQuery, Gtk.Label(titleQuery))
		page2 = notebook.append_page(tabEdit,  Gtk.Label(titleEdit))
		page3 = notebook.append_page(tabDB,    Gtk.Label(titleDB))

		pages[page1] = tabQuery
		pages[page2] = tabEdit
		pages[page3] = tabDB

		self.__pages = pages

		notebook.set_current_page(page1)
		tabQuery.setActive()

		boxOuter.pack_start(vocInOut, True,  True,  0)
		boxOuter.pack_start(notebook, False, False, 0)

		self.add(boxOuter)

		self.connect    ('destroy',self.__handlerDestroy)
		notebook.connect('switch-page',self.__handlerPageChanged)

		(winWidth, winHeight) = self.get_size()
		self.resize(winWidth + 250, winHeight + 75)
