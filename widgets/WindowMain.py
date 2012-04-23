#coding=utf8

import pygtk
import gtk

from . import *
from VocInOut import *
from TabEdit import *
from TabQuery import *
from TabDB import *

class WindowMain:
	def handlerDestroy(self, widget, data=None):
		gtk.mainquit()

	def handlerPageChanged(self, widget, page, page_num, data=None):
		self.pages[page_num].setActive()

	def __init__(self, db):
		db       = db
		vocInOut = VocInOut()

		window   = gtk.Window(gtk.WINDOW_TOPLEVEL)
		boxOuter = gtk.HBox(False, 4)
		notebook = gtk.Notebook()


		tabQuery = TabQuery(db, vocInOut)
		tabEdit  = TabEdit  (db, vocInOut)
		tabDB    = TabDB   (db, vocInOut)

		pages = {}

		page1 = notebook.append_page(tabQuery.getWidget(), gtk.Label('Abfrage'))
		page2 = notebook.append_page(tabEdit.getWidget(),  gtk.Label('Vokabeln'))
		page3 = notebook.append_page(tabDB.getWidget(),    gtk.Label('DB'))

		pages[page1] = tabQuery
		pages[page2] = tabEdit
		pages[page3] = tabDB

		self.pages = pages

		notebook.set_current_page(page1)
		tabQuery.setActive()

		boxOuter.pack_start(vocInOut.getWidget(), True,  True,  0)
		boxOuter.pack_start(notebook,             False, False, 0)

		window.add(boxOuter)

		window.connect  ('destroy',self.handlerDestroy)
		notebook.connect('switch-page',self.handlerPageChanged)

		notebook.show()
		boxOuter.show()

		(winWidth, winHeight) = window.get_size()
		window.resize(winWidth + 150, winHeight + 150)

		window.show()

