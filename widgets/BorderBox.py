#coding=utf8

import pygtk
import gtk

class BorderBox:
	def __init__(self):
		self.boxButtons = gtk.VBox(False,4)

		self.stateDependant  = []
		self.stateAssignment = {}
	
	def addButton(self, caption, handler, states = None):
		button = gtk.Button(caption)

		self.boxButtons.pack_start(button, False, False, 0)

		button.connect('clicked', handler)

		button.show()

		self.addToStates(button, states)
	
	def addSeparator(self):
		separator = gtk.HSeparator()
		
		self.boxButtons.pack_start(separator, False, False, 0)

		separator.show()
	
	def addWidget(self, widget, states = None):
		self.boxButtons.pack_start(widget, False, False, 0)

		widget.show()

		self.addToStates(widget, states)
	
	def addLabel(self, caption):
		label = gtk.Label(caption)

		self.boxButtons.pack_start(label, False, False, 0)

		label.show()
	
	def show(self):
		self.boxButtons.show()
	
	def getWidget(self):
		return self.boxButtons

	def addToStates(self, widget, states):
		if not states:
			return

		self.stateDependant.append(widget)

		for i_state in states:
			widgetlist = []
			if i_state in self.stateAssignment.keys():
				widgetlist = self.stateAssignment[i_state]

			widgetlist.append(widget)
			self.stateAssignment[i_state] = widgetlist
	
	def setState(self, state):
		if state not in self.stateAssignment.keys():
			widgetlist = []
		else:
			widgetlist = self.stateAssignment[state]

		for i_widget in self.stateDependant:
			if i_widget in widgetlist:
				sensitivity = True
			else:
				sensitivity = False
			i_widget.set_sensitive(sensitivity)
