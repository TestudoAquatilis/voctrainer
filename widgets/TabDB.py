#coding=utf8

import pygtk
import gtk
import pango

from ButtonBox import *

class TabDB:
	def handlerResetLevel(self, widget, data=None):
		self.db.resetLevel()

	def __init__(self, db, inOut):
		self.db    = db
		self.inOut = inOut

		buttonBox  = ButtonBox()

		buttonBox.add('Fortschritt zurücksetzen', self.handlerResetLevel)

		buttonBox.show()

		self.widget = buttonBox.getWidget()
	
	def getWidget(self):
		return self.widget

	def setActive(self):
		self.inOut.clearData()
