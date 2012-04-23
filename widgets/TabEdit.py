#coding=utf8

import pygtk
import gtk
import pango

from BorderBox import *

class TabEdit:
	def handlerClear(self, widget, data=None):
		self.inOut.clearData()

	def handlerInsert(self, widget, data=None):
		entries = self.inOut.getData()

		if len(entries['Deutsch']) == 0 or len(entries['Kana']) == 0:
			return

		self.db.addVoc(entries)

	def __init__(self, db, inOut):
		self.db    = db
		self.inOut = inOut

		borderBox  = BorderBox()

		borderBox.addButton('Eingabefelder leeren', self.handlerClear)
		borderBox.addButton('Vokabel einfügen',     self.handlerInsert)

		borderBox.show()
		
		self.widget = borderBox.getWidget()

	def getWidget(self):
		return self.widget

	def setActive(self):
		self.inOut.clearData()
