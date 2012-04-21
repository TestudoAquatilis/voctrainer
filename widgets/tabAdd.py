import pygtk
import gtk

class TabAdd:

	def handlerInsert(self, widget, data=None):
		deutsch = self.entryDeutsch.get_text()
		kana    = self.entryKana.get_text()
		kanji   = self.entryKanji.get_text()
		typ     = self.entryTyp.get_text()
		info    = self.entryInfo.get_text()

		if len(deutsch) == 0 or len(kana) == 0:
			return

		self.db.addVoc (deutsch, kana, kanji, typ, info)

	def __init__(self, db):
		self.db = db

		self.table = gtk.Table(2, 5, False)

		self.entryDeutsch = gtk.Entry()
		self.entryKana    = gtk.Entry()
		self.entryKanji   = gtk.Entry()
		self.entryTyp     = gtk.Entry()
		self.entryInfo    = gtk.Entry()
		
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

		self.buttonInsert = gtk.Button('Einfuegen')
		self.buttonTest   = gtk.Button('Test')

		self.boxOuter   = gtk.VBox(False,4)
		self.boxButtons = gtk.HBox(False,4)

		self.boxButtons.pack_start(self.buttonInsert, True, True, 0)
		self.boxButtons.pack_start(self.buttonTest, True, True, 0)

		self.boxOuter.pack_start(self.table, True, True, 0)
		self.boxOuter.pack_start(self.boxButtons, True, True, 0)

		self.buttonInsert.connect("clicked", self.handlerInsert)

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

		self.table.show()

		self.buttonInsert.show()
		self.buttonTest.show()

		self.boxButtons.show()
		self.boxOuter.show()
		
		self.widget = self.boxOuter

	def getWidget(self):
		return self.widget
