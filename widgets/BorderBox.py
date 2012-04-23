#coding=utf8

import pygtk
import gtk

class BorderBox:
	def __init__(self):
		self.boxButtons = gtk.VBox(False,4)
	
	def addButton(self, caption, handler):
		button = gtk.Button(caption)

		self.boxButtons.pack_start(button, False, False, 0)

		button.connect('clicked', handler)

		button.show()
	
	def addSeparator(self):
		separator = gtk.HSeparator()
		
		self.boxButtons.pack_start(separator, False, False, 0)

		separator.show()
	
	def addWidget(self, widget):
		self.boxButtons.pack_start(widget, False, False, 0)

		widget.show()
	
	def addLabel(self, caption):
		label = gtk.Label(caption)

		self.boxButtons.pack_start(label, False, False, 0)

		label.show()
	
	def show(self):
		self.boxButtons.show()
	
	def getWidget(self):
		return self.boxButtons
