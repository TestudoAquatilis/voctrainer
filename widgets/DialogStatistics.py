from gi.repository import Gtk

import config

class DialogStatistics(Gtk.Dialog):
	"""
	A Gtk.Dialog showing statistics about learning progress
	and amount of vocabulary.
	"""

	def __init__(self, db):
		strTitle = config.getDisplayString('DiaStTitle')

		Gtk.Dialog.__init__(self, strTitle, buttons = (Gtk.STOCK_OK, Gtk.ResponseType.OK))

		statistics = db.getStatistics()

		currentAmount = db.getAmountOfCurrentVocab()

		table = Gtk.Table(3, len(statistics) + 6, False)

		labelLeft  = Gtk.Label(config.getDisplayString('DiaStHeadLevel'))
		labelRight = Gtk.Label(config.getDisplayString('DiaStHeadAmount'))

		labelXOpt = Gtk.AttachOptions.FILL

		table.attach(labelLeft,  0, 1, 0, 1, labelXOpt, xpadding=4, ypadding=4)
		table.attach(labelRight, 2, 3, 0, 1, xpadding=4, ypadding=4)

		separator = Gtk.Separator(orientation = Gtk.Orientation.HORIZONTAL)
		table.attach(separator, 0, 3, 1, 2)

		separator = Gtk.Separator(orientation = Gtk.Orientation.VERTICAL)
		table.attach(separator, 1, 2, 0, len(statistics) + 6, labelXOpt)

		vocsum = 0

		for i_val in statistics.values():
			vocsum += i_val

		i = 2

		for i_key in statistics.keys():
			labelLeft   = Gtk.Label(i_key)
			progressbar = Gtk.ProgressBar()
			progressbar.set_text(str(statistics[i_key]))
			progressbar.set_show_text(True)
			progressbar.set_fraction(statistics[i_key]/vocsum)

			table.attach(labelLeft,   0, 1, i, i+1, labelXOpt, xpadding=4, ypadding=4)
			table.attach(progressbar, 2, 3, i, i+1, xpadding=4, ypadding=2)

			i      += 1

		separator = Gtk.Separator(orientation = Gtk.Orientation.HORIZONTAL)
		table.attach(separator, 0, 3, i, i+1)

		i += 1

		labelLeft  = Gtk.Label(config.getDisplayString('DiaStSum'))
		labelRight = Gtk.Label(vocsum)

		table.attach(labelLeft,  0, 1, i, i+1, labelXOpt, xpadding=4, ypadding=4)
		table.attach(labelRight, 2, 3, i, i+1, xpadding=4, ypadding=4)

		i += 1

		separator = Gtk.Separator(orientation = Gtk.Orientation.HORIZONTAL)
		table.attach(separator, 0, 3, i, i+1)

		i += 1

		toolTip = config.getTooltipString('DiaStCurAmount')
		labelLeft  = Gtk.Label(config.getDisplayString('DiaStCurAmount'))
		progressbar = Gtk.ProgressBar()
		progressbar.set_text(str(currentAmount))
		progressbar.set_show_text(True)
		progressbar.set_fraction(currentAmount/vocsum)
		if toolTip:
			progressbar.set_tooltip_text(toolTip)
			labelLeft.set_tooltip_text(toolTip)

		table.attach(labelLeft,   0, 1, i, i+1, labelXOpt, xpadding=4, ypadding=4)
		table.attach(progressbar, 2, 3, i, i+1, xpadding=4, ypadding=2)

		table.show_all()

		self.get_content_area().add(table)

