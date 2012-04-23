#coding=utf8

import pygtk
import gtk
import pango

from BorderBox import *

class TabDB:
	def handlerResetLevel(self, widget, data=None):
		self.db.resetLevel()

	def __init__(self, db, inOut):
		self.db    = db
		self.inOut = inOut

		borderBox  = BorderBox()

		borderBox.addButton('Fortschritt zurücksetzen', self.handlerResetLevel)

		borderBox.show()

		self.widget = borderBox.getWidget()
	
	def getWidget(self):
		return self.widget

	def setActive(self):
		self.inOut.clearData()
		self.inOut.setSensitive(False)
