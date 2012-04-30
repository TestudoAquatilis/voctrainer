from gi.repository import Gtk

import config

class BorderBox(Gtk.Box):
	"""
	A box containing control widgets.

	Used for abstraction from widget creation, packing, showing, connecting, ...
	"""

	def __init__(self):
		"""
		Constructor.
		"""

		Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=4)

		self.__stateDependant  = []
		self.__stateAssignment = {}
	
	def addButton(self, buttonId, handler, states=None):
		"""
		Add a button to the BorderBox.

		@param buttonId id of the button string and tooltip
		@param handler Gtk-handler to call when button is clicked
		@param states an array of statenames, the button is sensitive in or None if button is always sensitive
		"""

		caption = config.getDisplayString(buttonId)
		toolTip = config.getTooltipString(buttonId)

		button = Gtk.Button(caption, use_underline=True)

		self.pack_start(button, False, False, 0)

		button.connect('clicked', handler)

		if toolTip:
			button.set_tooltip_text(toolTip)

		self.__addToStates(button, states)
	
	def addSeparator(self):
		"""
		Add a separator to the BorderBox.
		"""

		separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
		
		self.pack_start(separator, False, False, 0)

	def addWidget(self, widget, states = None, toolTipId=None):
		"""
		Add a given Gtk.Widget to the BorderBox.

		@param widget the widget to add
		@param states an array of statenames, the button is sensitive in or None if button is always sensitive
		"""

		toolTip = config.getTooltipString(toolTipId)

		self.pack_start(widget, False, False, 0)

		if toolTip:
			widget.set_tooltip_text(toolTip)

		self.__addToStates(widget, states)
	
	def addLabel(self, caption):
		"""
		Add a label to the BorderBox.

		@param caption the caption of the label to add
		"""

		label = Gtk.Label(caption)

		self.pack_start(label, False, False, 0)

		label.show()

	def __addToStates(self, widget, states):
		"""
		The given widget should be made sensitive in the given states.

		@param widget the Gtk.Widget to add
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
