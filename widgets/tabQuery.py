import pygtk
import gtk
import pango

class TabQuery:
	def getNextVoc(self):
		self.nextVoc = self.db.getNext()
	
	def showVoc(self):
		if len(self.nextVoc.keys()) < 5:
			return

		self.entryDeutsch.set_text(self.nextVoc['Deutsch'])
		self.entryKana.set_text('')
		self.entryKanji.set_text('')
		self.entryTyp.set_text(self.nextVoc['Typ'])
		self.entryInfo.set_text('')

	def solve(self):
		if len(self.nextVoc.keys()) < 5:
			return

		self.entryDeutsch.set_text(self.nextVoc['Deutsch'])
		self.entryKana.set_text(self.nextVoc['Kana'])
		self.entryKanji.set_text(self.nextVoc['Kanji'])
		self.entryTyp.set_text(self.nextVoc['Typ'])
		self.entryInfo.set_text(self.nextVoc['Info'])

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

	def __init__(self, db):
		self.db = db

		self.boxOuter   = gtk.HBox(False, 4)
		self.boxButtons = gtk.VBox(False, 4)

		self.table = gtk.Table(2, 5, False)

		self.fontLarge  = pango.FontDescription('20')
		self.fontMedium = pango.FontDescription('16')
		
		# Buttons
		self.buttonKnown    = gtk.Button('Gewusst')
		self.buttonNotKnown = gtk.Button('Nicht gewusst')
		self.buttonSolve    = gtk.Button('Loesen')
		self.buttonNext     = gtk.Button('Naechste')

		self.boxButtons.pack_start(self.buttonNext, True, True, 0)
		self.boxButtons.pack_start(self.buttonSolve, True, True, 0)
		self.boxButtons.pack_start(self.buttonKnown, True, True, 0)
		self.boxButtons.pack_start(self.buttonNotKnown, True, True, 0)


		# Entries
		self.entryDeutsch = gtk.Entry()
		self.entryKana    = gtk.Entry()
		self.entryKanji   = gtk.Entry()
		self.entryTyp     = gtk.Entry()
		self.entryInfo    = gtk.Entry()

		self.entryDeutsch.modify_font(self.fontMedium)
		self.entryKana.modify_font(self.fontMedium)
		self.entryKanji.modify_font(self.fontLarge)
		#self.entryTyp.modify_font(self.fontLarge)
		self.entryInfo.modify_font(self.fontMedium)
		
		self.labelDeutsch = gtk.Label('Deutsch:')
		self.labelKana    = gtk.Label('Kana:')
		self.labelKanji   = gtk.Label('Kanji:')
		self.labelTyp     = gtk.Label('Typ:')
		self.labelInfo    = gtk.Label('Info:')

		self.table.attach(self.labelDeutsch, 0, 1, 0, 1)
		self.table.attach(self.labelKana,    0, 1, 1, 2)
		self.table.attach(self.labelKanji,   0, 1, 2, 3)
		self.table.attach(self.labelTyp,     0, 1, 3, 4)
		self.table.attach(self.labelInfo,    0, 1, 4, 5)

		self.table.attach(self.entryDeutsch, 1, 2, 0, 1)
		self.table.attach(self.entryKana,    1, 2, 1, 2)
		self.table.attach(self.entryKanji,   1, 2, 2, 3)
		self.table.attach(self.entryTyp,     1, 2, 3, 4)
		self.table.attach(self.entryInfo,    1, 2, 4, 5)

		# Packing
		self.boxOuter.pack_start(self.table, True, True, 0)
		self.boxOuter.pack_start(self.boxButtons, True, True, 0)


		# Show
		self.entryDeutsch.show()
		self.entryKana.show()
		self.entryKanji.show()
		self.entryTyp.show()
		self.entryInfo.show()

		self.labelDeutsch.show()
		self.labelKana.show()
		self.labelKanji.show()
		self.labelTyp.show()
		self.labelInfo.show()

		self.buttonNext.connect('clicked', self.handlerNext)
		self.buttonSolve.connect('clicked', self.handlerSolve)
		self.buttonKnown.connect('clicked', self.handlerKnown)
		self.buttonNotKnown.connect('clicked', self.handlerNotKnown)

		self.buttonNext.show()
		self.buttonSolve.show()
		self.buttonKnown.show()
		self.buttonNotKnown.show()


		self.table.show()
		self.boxButtons.show()
		self.boxOuter.show()

		self.nextVoc = db.getNext()
		self.showVoc()
		
		self.widget = self.boxOuter

	def getWidget(self):
		return self.widget
