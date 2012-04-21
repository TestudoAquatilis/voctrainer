#coding=utf8
import pygtk
import gtk
import pango

class TabDB:
	def handlerInit(self, widget, data=None):
		dia = gtk.MessageDialog(None, 0, gtk.MESSAGE_WARNING, gtk.BUTTONS_YES_NO)

		dia_res = dia.run()
		dia.hide()

		if dia_res == gtk.RESPONSE_YES:
			self.db.create()

	def __init__(self, db):
		self.db = db
		self.boxButtons = gtk.VBox(False, 4)

		# Buttons
		self.buttonInit = gtk.Button('Initialisieren')

		buttonExpand = False
		buttonFill   = False
		self.boxButtons.pack_start(self.buttonInit, buttonExpand, buttonFill, 0)

		self.buttonInit.connect('clicked', self.handlerInit)

		self.buttonInit.show()
		self.boxButtons.show()

		self.widget = self.boxButtons
	
	def getWidget(self):
		return self.widget
