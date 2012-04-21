#coding=utf8
import pygtk
import gtk

import widgets.tabAdd
import widgets.tabQuery

class WindowMain:
	def destroy(self, widget, data=None):
		gtk.mainquit()

	def __init__(self, db):
		self.db     = db
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.notebook = gtk.Notebook()
		
		self.tabAdd = widgets.tabAdd.TabAdd(db)
		self.notebook.append_page(self.tabAdd.getWidget(), gtk.Label('Hinzufügen'))

		self.tabQuery = widgets.tabQuery.TabQuery(db)
		self.notebook.append_page(self.tabQuery.getWidget(), gtk.Label('Abfragen'))

		self.window.add(self.notebook)
		self.window.connect('destroy',self.destroy)

		self.notebook.show()
		self.window.show()


