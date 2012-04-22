#coding=utf8
import pygtk
import gtk

from . import *
from VocInOut import *
from TabAdd import *
from TabQuery import *
from TabDB import *

class WindowMain:
	def destroy(self, widget, data=None):
		gtk.mainquit()

	def __init__(self, db):
		db     = db

		boxOuter = gtk.HBox(False, 4)

		window = gtk.Window(gtk.WINDOW_TOPLEVEL)

		vocInOut = VocInOut()

		notebook = gtk.Notebook()
		
		tabAdd = TabAdd(db, vocInOut)
		notebook.append_page(tabAdd.getWidget(), gtk.Label('Hinzufügen'))

		tabQuery = TabQuery(db, vocInOut)
		notebook.append_page(tabQuery.getWidget(), gtk.Label('Abfragen'))

		tabDB = TabDB(db, vocInOut)
		notebook.append_page(tabDB.getWidget(), gtk.Label('Datenbank'))

		boxOuter.pack_start(vocInOut.getWidget(), True, True, 0)
		boxOuter.pack_start(notebook, False, False, 0)

		window.add(boxOuter)
		window.connect('destroy',self.destroy)

		notebook.show()
		boxOuter.show()
		window.show()

		testData = {'Deutsch':'Test'}

