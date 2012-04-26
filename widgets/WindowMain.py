#coding=utf8

from gi.repository import Gtk

from . import *
from .VocInOut import *
from .TabEdit import *
from .TabQuery import *
from .TabDB import *

class WindowMain(Gtk.Window):
	"""
	Main Window of the Program.

	Here the widgets are put in
	"""

	def __handlerDestroy(self, widget, data=None):
		Gtk.mainquit()

	def __handlerPageChanged(self, widget, page, page_num, data=None):
		self.__pages[page_num].setActive()

	def __init__(self, db):
		"""
		Constructor.

		@param db The object, data is handled in as database.DBVoc
		@see database.DBVoc.DBVoc
		"""

		Gtk.Window.__init__(self, title='Vokabeltrainer')

		db       = db
		vocInOut = VocInOut()

		vocInOut.setTypList(db.getTypList())

		boxOuter = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		notebook = Gtk.Notebook()

		tabQuery = TabQuery(db, vocInOut)
		tabEdit  = TabEdit (db, vocInOut)
		tabDB    = TabDB   (db, vocInOut)

		pages = {}

		page1 = notebook.append_page(tabQuery.getWidget(), Gtk.Label('Abfrage'))
		page2 = notebook.append_page(tabEdit.getWidget(),  Gtk.Label('Vokabeln'))
		page3 = notebook.append_page(tabDB.getWidget(),    Gtk.Label('DB'))

		pages[page1] = tabQuery
		pages[page2] = tabEdit
		pages[page3] = tabDB

		self.__pages = pages

		notebook.set_current_page(page1)
		tabQuery.setActive()

		boxOuter.pack_start(vocInOut.getWidget(), True,  True,  0)
		boxOuter.pack_start(notebook,             False, False, 0)

		self.add(boxOuter)

		self.connect    ('destroy',self.__handlerDestroy)
		notebook.connect('switch-page',self.__handlerPageChanged)

		(winWidth, winHeight) = self.get_size()
		self.resize(winWidth + 150, winHeight + 150)

