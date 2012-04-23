#coding=utf8

import pygtk
import gtk

class ButtonBox:
	def __init__(self):
		self.boxButtons = gtk.VBox(False,4)
	
	def add(self, caption, handler):
		button = gtk.Button(caption)

		self.boxButtons.pack_start(button, False, False, 0)

		button.connect('clicked', handler)

		button.show()
	
	def addSeparator(self):
		separator = gtk.HSeparator()
		
		self.boxButtons.pack_start(separator, False, False, 0)

		separator.show()
	
	def show(self):
		self.boxButtons.show()
	
	def getWidget(self):
		return self.boxButtons
