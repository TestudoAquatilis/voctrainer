#coding=utf8
import pygtk
import gtk
import pango

from ButtonBox import *

class TabDB:
	def handlerInit(self, widget, data=None):
		dia = gtk.MessageDialog(None, 0, gtk.MESSAGE_WARNING, gtk.BUTTONS_YES_NO)

		dia_res = dia.run()
		dia.hide()

		if dia_res == gtk.RESPONSE_YES:
			self.db.create()
	
	def handlerResetLevel(self, widget, data=None):
		self.db.resetLevel()

	def __init__(self, db, inOut):
		self.db    = db
		self.inOut = inOut

		buttonBox = ButtonBox()

		buttonBox.add('Initialisieren',           self.handlerInit)
		buttonBox.add('Fortschritt zurücksetzen', self.handlerResetLevel)

		buttonBox.show()

		self.widget = buttonBox.getWidget()
	
	def getWidget(self):
		return self.widget
