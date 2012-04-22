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

	def __init__(self, db, inOut):
		self.db    = db
		self.inOut = inOut

		boxButtons = gtk.VBox(False, 4)

		# Buttons
		buttonInit = gtk.Button('Initialisieren')

		buttonExpand = False
		buttonFill   = False
		boxButtons.pack_start(buttonInit, buttonExpand, buttonFill, 0)

		buttonInit.connect('clicked', self.handlerInit)

		buttonInit.show()
		boxButtons.show()

		self.widget = boxButtons
	
	def getWidget(self):
		return self.widget
