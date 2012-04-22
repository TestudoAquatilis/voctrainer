#coding=utf8
import pygtk
import gtk
import pango

class TabAdd:

	def handlerClear(self, widget, data=None):
		self.inOut.clearData()

	def handlerInsert(self, widget, data=None):
		entries = self.inOut.getData()

		if len(entries['Deutsch']) == 0 or len(entries['Kana']) == 0:
			return

		self.db.addVoc(entries['Deutsch'], entries['Kana'], entries['Kanji'], entries['Typ'], entries['Info'])

	def __init__(self, db, inOut):
		self.db = db
		self.inOut = inOut

		buttonClear = gtk.Button('Leeren')
		buttonInsert = gtk.Button('Einfügen')

		boxButtons = gtk.VBox(False,4)

		buttonExpand = False
		buttonFill   = False
		boxButtons.pack_start(buttonClear, buttonExpand, buttonFill, 0)
		boxButtons.pack_start(buttonInsert, buttonExpand, buttonFill, 0)

		buttonClear.connect('clicked', self.handlerClear)
		buttonInsert.connect('clicked', self.handlerInsert)

		buttonClear.show()
		buttonInsert.show()
		boxButtons.show()
		
		self.widget = boxButtons

	def getWidget(self):
		return self.widget
