#coding=utf8

from gi.repository import Pango

__fonts = {
		'Medium': '20',
		'Kanji':  'IPAMincho 40',
		'Kana':   'IPAMincho 20',
	}

__filenames = {
		'Database': 'vocabulary.db',
	}

__displayStrings = {
		# Database
		'DBLang1'  : 'Deutsch',
		'DBLang2'  : 'Kana',
		'DBSpecial': 'Kanji',
		'DBType'   : 'Typ',
		'DBInfo'   : 'Info',
		# WindowMain
		'WindowMainTitle': 'Vokabeltrainer',
		'TabQueryTitle'  : 'Abfrage',
		'TabEditTitle'   : 'Vokablen',
		'TabDBTitle'     : 'DB',
		# TabQuery
		'TQueryNext'     : 'Nächste',
		'TQuerySolve'    : '_Lösen',
		'TQueryKnown'    : '_Gewusst',
		'TQueryNotKnown' : '_Nicht Gewusst',
		'TQueryModify'   : 'Vokabel Ändern',
		'TQueryDelete'   : 'Vokabel Löschen',
		# TabEdit
		'TEditErrorAlreadyExists' : 'Vokabel existiert bereits!',
		'TEditClear'  : 'Eingabefelder leeren',
		'TEditSearch' : '_Suchen',
		'TEditInsert' : 'Vokable _Einfügen',
		'TEditModify' : 'Vokabel Ändern',
		'TEditDelete' : 'Vokabel Löschen',
		# TabDB
		'TDBFCExport' : 'Exportiere DB in Datei',
		'TDBFCImport' : 'Importiere DB aus Datei',
		'TDBFFCSV'    : 'CSV-Datei',
		'TDBDiaResetWarning' : 'Der gesamte Lernfortschritt wird damit zurückgesetzt!\nDieser Vorgang ist unwiderruflich! Fortfahren?',
		'TDBDiaShuffleInfo'  : 'Es wurden insgesamt %d Vokabeln neu gemischt.',
		'TDBShuffle'     : 'Neu mischen',
		'TDBReset'       : 'Fortschritt zurücksetzen',
		'TDBStatistics'  : 'Statistik',
		'TDBExport'      : 'Datenbank exportieren',
		'TDBImport'      : 'Datenbank importieren',
		# DialogStatistics
		'DiaStTitle' : 'Lernstatistik',
		'DiaStHeadLevel' : 'Stufe',
		'DiaStHeadAmount': 'Enthaltene Vokabeln',
		'DiaStSum'       : 'Summe',
	}

__tooltipStrings = {
		# TabQuery
		'TQueryNext'     : 'Zeige die nächste Vokabel.',
		'TQuerySolve'    : 'Zeige die Lösung.',
		'TQueryKnown'    : 'Vokabel gewusst...\nerst nach längerer Zeit wieder abfragen.',
		'TQueryNotKnown' : 'Vokabel nicht gewusst...\nrelativ früh wieder abfragen.',
		'TQueryModify'   : 'Modifizierte Vokabel in die Datenbank übernehmen.',
		'TQueryDelete'   : 'Löscht die Vokabel unwiderruflich aus der Datenbank!',
		# TabEdit
		'TEditClear'         : 'Leert die Eingabefelder, damit eine neue Vokabel eingegeben werden kann.',
		'TEditSearch'        : 'Sucht nach Vokabeln, die einen der eingegebenen Texte enthalten.',
		'TEditSearchResults' : 'Liste der Suchergebnisse.',
		'TEditInsert'        : 'Fügt die Vokabel in die Datenbank ein.',
		'TEditModify'        : 'Übernimmt die Veränderungen in die Datenbank.',
		'TEditDelete'        : 'Löscht die Vokabel unwiderruflich aus der Datenbank!',
		# TabDB
		'TDBShuffle'     : 'Durchmischt alle Vokablen neu,\ndie aktuell abzufragen sind.',
		'TDBReset'       : 'Setzt jeglichen gespeicherten Lernfortschritt zurück!\nAlle Vokabeln werden wie neu behandelt.\nDieser Schritt ist unwiderruflich!!!',
		'TDBStatistics'  : 'Zeigt eine Statistik über den Lernfortschritt',
		'TDBExport'      : 'Exportiert die Datenbank in eine CSV-Datei.',
		'TDBImport'      : 'Importiert Datenbankeinträge aus einer CSV-Datei',
	}

def getFont(id):
	"""
	Get the font for the given id.

	@param id the id of the font as string
	@return the font as pango FontDescription
	"""

	desc = ''

	if isinstance(id, str):
		if id in __fonts.keys():
			desc = __fonts[id]
	else:
		for i_id in id:
			if len(i_id) > 1:
				if i_id in __fonts.keys():
					desc = __fonts[i_id]
					break

	
	return Pango.FontDescription(desc)

def getFilename(id):
	"""
	Get the filename for the given id.

	@param id the id of the filename as string
	@return the filename as string
	"""

	result = None

	if id in __filenames.keys():
		result = __filenames[id]
	
	return result

def getDisplayString(id):
	"""
	Get the string to display from the given id.

	@param id the id of the string to display
	@return the string to display or '' if not found
	"""

	result = ''

	if id in __displayStrings.keys():
		result = __displayStrings[id]
	
	return result

def getTooltipString(id):
	"""
	Get the tooltip string for the given id.

	@param id the id of the tooltip string
	@return the tooltip string or None if not found
	"""

	result = None

	if id in __tooltipStrings.keys():
		result = __tooltipStrings[id]
	
	return result

