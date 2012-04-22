#coding=utf8
import pygtk
import gtk
import pango

from ButtonBox import *

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

		buttonBox = ButtonBox()

		buttonBox.add('Leeren', self.handlerClear)
		buttonBox.add('Einfügen', self.handlerInsert)

		buttonBox.show()
		
		self.widget = buttonBox.getWidget()

	def getWidget(self):
		return self.widget
