#coding=utf8

import pygtk
import gtk
import pango

from ButtonBox import *

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
		self.db.updateLevel(self.nextVoc, self.nextVoc['Level']+1)

	def notKnown(self):
		if len(self.nextVoc.keys()) < 6:
			return
		self.db.updateLevel(self.nextVoc, 0)

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

	def handlerUpdate(self, widget, data=None):
		entries = self.inOut.getData()
		self.db.modifyVoc(self.nextVoc, entries)
	
	def handlerDelete(self, widget, data=None):
		self.db.deleteVoc(self.nextVoc)
		self.getNextVoc()
		self.showVoc()

	def __init__(self, db, inOut):
		self.db    = db
		self.inOut = inOut

		buttonBox  = ButtonBox()

		buttonBox.add('Nächste',         self.handlerNext)
		buttonBox.addSeparator()
		buttonBox.add('Lösen',           self.handlerSolve)
		buttonBox.add('Gewusst',         self.handlerKnown)
		buttonBox.add('Nicht gewusst',   self.handlerNotKnown)
		buttonBox.addSeparator()
		buttonBox.add('Vokabel Ändern',  self.handlerUpdate)
		buttonBox.add('Vokabel Löschen', self.handlerDelete)

		buttonBox.show()

		self.widget = buttonBox.getWidget()

		self.nextVoc = db.getNext()
		
	def getWidget(self):
		return self.widget

	def setActive(self):
		self.getNextVoc()
		self.showVoc()
