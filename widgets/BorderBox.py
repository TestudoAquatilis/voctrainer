#coding=utf8

import pygtk
import gtk

class BorderBox:
	"""
	A box containing control widgets.

	Used for abstraction from widget creation, packing, showing, connecting, ...
	"""

	def __init__(self):
		"""
		Constructor.
		"""

		self.__boxButtons      = gtk.VBox(False,4)

		self.__stateDependant  = []
		self.__stateAssignment = {}
	
	def addButton(self, caption, handler, states=None):
		"""
		Add a button to the BorderBox.

		@param caption caption of the button to add
		@param handler gtk-handler to call when button is clicked
		@param states an array of statenames, the button is sensitive in or None if button is always sensitive
		"""

		button = gtk.Button(caption)

		self.__boxButtons.pack_start(button, False, False, 0)

		button.connect('clicked', handler)

		button.show()

		self.__addToStates(button, states)
	
	def addSeparator(self):
		"""
		Add a separator to the BorderBox.
		"""

		separator = gtk.HSeparator()
		
		self.__boxButtons.pack_start(separator, False, False, 0)

		separator.show()
	
	def addWidget(self, widget, states = None):
		"""
		Add a given gtk.Widget to the BorderBox.

		@param widget the widget to add
		@param states an array of statenames, the button is sensitive in or None if button is always sensitive
		"""

		self.__boxButtons.pack_start(widget, False, False, 0)

		widget.show()

		self.__addToStates(widget, states)
	
	def addLabel(self, caption):
		"""
		Add a label to the BorderBox.

		@param caption the caption of the label to add
		"""

		label = gtk.Label(caption)

		self.__boxButtons.pack_start(label, False, False, 0)

		label.show()
	
	def show(self):
		"""
		Make the BorderBox visible.
		"""

		self.__boxButtons.show()
	
	def getWidget(self):
		"""
		Get the gtk.Widget defining the BorderBox.

		@returns the gtk.Widget defining the BorderBox
		"""

		return self.__boxButtons

	def __addToStates(self, widget, states):
		"""
		The given widget should be made sensitive in the given states.

		@param widget the gtk.Widget to add
		@param states the list of statenames, the widget should be sensitive in or None for always sensitive
		"""

		if not states:
			return

		self.__stateDependant.append(widget)

		for i_state in states:
			widgetlist = []
			if i_state in self.__stateAssignment.keys():
				widgetlist = self.__stateAssignment[i_state]

			widgetlist.append(widget)
			self.__stateAssignment[i_state] = widgetlist
	
	def setState(self, state):
		"""
		Make all widgets listening on a state sensitive or insensitive according to given state.

		@param state state as string
		"""

		if state not in self.__stateAssignment.keys():
			widgetlist = []
		else:
			widgetlist = self.__stateAssignment[state]

		for i_widget in self.__stateDependant:
			if i_widget in widgetlist:
				sensitivity = True
			else:
				sensitivity = False
			i_widget.set_sensitive(sensitivity)
