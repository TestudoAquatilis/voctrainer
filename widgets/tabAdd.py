#coding=utf8
import pygtk
import gtk
import pango

class TabAdd:

	def handlerInsert(self, widget, data=None):
		deutsch = self.entryDeutsch.get_text().decode('utf-8')
		kana    = self.entryKana.get_text().decode('utf-8')
		kanji   = self.entryKanji.get_text().decode('utf-8')
		typ     = self.entryTyp.get_text().decode('utf-8')
		#info    = self.entryInfo.get_text().decode('utf-8')
		info    = self.entryInfo.get_buffer().get_text(self.entryInfo.get_buffer().get_start_iter(), self.entryInfo.get_buffer().get_end_iter()).decode('utf-8')

		if len(deutsch) == 0 or len(kana) == 0:
			return

		self.db.addVoc (deutsch, kana, kanji, typ, info)

	def __init__(self, db):
		self.db = db

		self.table = gtk.Table(2, 5, False)

		self.fontLarge  = pango.FontDescription('20')
		self.fontMedium = pango.FontDescription('16')

		self.entryDeutsch = gtk.Entry()
		self.entryKana    = gtk.Entry()
		self.entryKanji   = gtk.Entry()
		self.entryTyp     = gtk.Entry()
		self.entryInfo    = gtk.TextView()
		
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

		labelXOpt = 0
		labelYOpt = 0
		self.table.attach(self.labelDeutsch, 0, 1, 0, 1, labelXOpt, labelYOpt)
		self.table.attach(self.labelKana,    0, 1, 1, 2, labelXOpt, labelYOpt)
		self.table.attach(self.labelKanji,   0, 1, 2, 3, labelXOpt, labelYOpt)
		self.table.attach(self.labelTyp,     0, 1, 3, 4, labelXOpt, labelYOpt)
		self.table.attach(self.labelInfo,    0, 1, 4, 5, labelXOpt, labelYOpt)

		entryXOpt    = gtk.EXPAND|gtk.FILL
		entryYOpt    = gtk.FILL
		entryYOptExp = gtk.EXPAND|gtk.FILL
		self.table.attach(self.entryDeutsch, 1, 2, 0, 1, entryXOpt, entryYOpt)
		self.table.attach(self.entryKana,    1, 2, 1, 2, entryXOpt, entryYOpt)
		self.table.attach(self.entryKanji,   1, 2, 2, 3, entryXOpt, entryYOpt)
		self.table.attach(self.entryTyp,     1, 2, 3, 4, entryXOpt, entryYOpt)
		self.table.attach(self.entryInfo,    1, 2, 4, 5, entryXOpt, entryYOptExp)

		self.buttonInsert = gtk.Button('Einfügen')

		self.boxOuter   = gtk.HBox(False,4)
		self.boxButtons = gtk.VBox(False,4)

		self.boxButtons.pack_start(self.buttonInsert, False, False, 0)

		self.boxOuter.pack_start(self.table, True, True, 0)
		self.boxOuter.pack_start(self.boxButtons, False, False, 0)

		self.buttonInsert.connect('clicked', self.handlerInsert)

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

		self.boxButtons.show()
		self.boxOuter.show()
		
		self.widget = self.boxOuter

	def getWidget(self):
		return self.widget
