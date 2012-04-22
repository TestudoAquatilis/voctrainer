#coding=utf8
import pygtk
import gtk
import pango

class TabQuery:
	def getNextVoc(self):
		self.nextVoc = self.db.getNext()
	
	def showVoc(self):
		if len(self.nextVoc.keys()) < 5:
			return
		data = self.nextVoc.copy()
		data['Kana'] = ''
		data['Kanji'] = ''
		data['Info'] = ''
		self.inOut.setData(data)

	def solve(self):
		if len(self.nextVoc.keys()) < 5:
			return
		self.inOut.setData(self.nextVoc)

	def known(self):
		if len(self.nextVoc.keys()) < 6:
			return
		self.db.updateLevel(self.nextVoc['Deutsch'], self.nextVoc['Kana'], self.nextVoc['Level']+1)

	def notKnown(self):
		if len(self.nextVoc.keys()) < 6:
			return
		self.db.updateLevel(self.nextVoc['Deutsch'], self.nextVoc['Kana'], 0)

	def handlerNext(self, widget, data=None):
		self.getNextVoc()
		self.showVoc()

	def handlerSolve(self, widget, data=None):
		self.solve()

	def handlerKnown(self, widget, data=None):
		self.known()
		self.getNextVoc()
		self.showVoc()
	
	def handlerNotKnown(self, widget, data=None):
		self.notKnown()
		self.getNextVoc()
		self.showVoc()

	def __init__(self, db, inOut):
		self.db = db
		self.inOut = inOut

		boxButtons = gtk.VBox(False, 4)

		# Buttons
		buttonKnown    = gtk.Button('Gewusst')
		buttonNotKnown = gtk.Button('Nicht gewusst')
		buttonSolve    = gtk.Button('Lösen')
		buttonNext     = gtk.Button('Nächste')

		buttonExpand = False
		buttonFill   = False
		boxButtons.pack_start(buttonNext, buttonExpand, buttonFill, 0)
		boxButtons.pack_start(buttonSolve, buttonExpand, buttonFill, 0)
		boxButtons.pack_start(buttonKnown, buttonExpand, buttonFill, 0)
		boxButtons.pack_start(buttonNotKnown, buttonExpand, buttonFill, 0)

		buttonNext.connect('clicked', self.handlerNext)
		buttonSolve.connect('clicked', self.handlerSolve)
		buttonKnown.connect('clicked', self.handlerKnown)
		buttonNotKnown.connect('clicked', self.handlerNotKnown)

		buttonNext.show()
		buttonSolve.show()
		buttonKnown.show()
		buttonNotKnown.show()

		boxButtons.show()

		self.nextVoc = db.getNext()
		self.showVoc()
		
		self.widget = boxButtons

	def getWidget(self):
		return self.widget
