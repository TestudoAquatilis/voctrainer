#coding=utf8

import pygtk
import gtk
import pango

class VocInOut:
	class entryInOut:
		def __init__(self, entry):
			self.entry = entry

		def getText(self):
			return self.entry.get_text().decode('utf-8')

		def setText(self, text):
			self.entry.set_text(text)
	
	class textViewInOut:
		def __init__(self, textView):
			self.textView = textView

		def getText(self):
			return self.textView.get_buffer().get_text(self.textView.get_buffer().get_start_iter(), self.textView.get_buffer().get_end_iter()).decode('utf-8')

		def setText(self, text):
			self.textView.get_buffer().set_text(text)

	def __init__(self):
		table = gtk.Table(2, 5, False)

		fontLarge  = pango.FontDescription('24')
		fontMedium = pango.FontDescription('16')

		entryDeutsch = gtk.Entry()
		entryKana    = gtk.Entry()
		entryKanji   = gtk.Entry()
		entryTyp     = gtk.Entry()
		entryInfo    = gtk.TextView()
		
		entryDeutsch.modify_font(fontMedium)
		entryKana.modify_font(fontMedium)
		entryKanji.modify_font(fontLarge)
		#entryTyp.modify_font(fontLarge)
		entryInfo.modify_font(fontMedium)

		labelDeutsch = gtk.Label('Deutsch:')
		labelKana    = gtk.Label('Kana:')
		labelKanji   = gtk.Label('Kanji:')
		labelTyp     = gtk.Label('Typ:')
		labelInfo    = gtk.Label('Info:')

		labelXOpt = 0
		labelYOpt = 0

		table.attach(labelDeutsch, 0, 1, 0, 1, labelXOpt, labelYOpt)
		table.attach(labelKana,    0, 1, 1, 2, labelXOpt, labelYOpt)
		table.attach(labelKanji,   0, 1, 2, 3, labelXOpt, labelYOpt)
		table.attach(labelTyp,     0, 1, 3, 4, labelXOpt, labelYOpt)
		table.attach(labelInfo,    0, 1, 4, 5, labelXOpt, labelYOpt)

		entryXOpt    = gtk.EXPAND|gtk.FILL
		entryYOpt    = gtk.FILL
		entryYOptExp = gtk.EXPAND|gtk.FILL

		table.attach(entryDeutsch, 1, 2, 0, 1, entryXOpt, entryYOpt)
		table.attach(entryKana,    1, 2, 1, 2, entryXOpt, entryYOpt)
		table.attach(entryKanji,   1, 2, 2, 3, entryXOpt, entryYOpt)
		table.attach(entryTyp,     1, 2, 3, 4, entryXOpt, entryYOpt)
		table.attach(entryInfo,    1, 2, 4, 5, entryXOpt, entryYOptExp)

		entryDeutsch.show()
		entryKana.show()
		entryKanji.show()
		entryTyp.show()
		entryInfo.show()

		labelDeutsch.show()
		labelKana.show()
		labelKanji.show()
		labelTyp.show()
		labelInfo.show()

		table.show()

		self.widget = table

		entries = {}
		entries['Deutsch'] = self.entryInOut(entryDeutsch)
		entries['Kana']    = self.entryInOut(entryKana)
		entries['Kanji']   = self.entryInOut(entryKanji)
		entries['Typ']     = self.entryInOut(entryTyp)
		entries['Info']    = self.textViewInOut(entryInfo)

		self.entries = entries

	def getWidget(self):
		return self.widget

	def getData(self):
		result = {}

		for i_key in self.entries.keys():
			result[i_key] = self.entries[i_key].getText()

		return result
	
	def setData(self, data):
		for i_key in self.entries.keys():
			if i_key in data.keys():
				self.entries[i_key].setText(data[i_key])
	
	def clearData(self):
		for i_val in self.entries.values():
			i_val.setText('')
