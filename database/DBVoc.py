import sqlite3
import datetime
import random

class DBVoc:
	"""
	Wrapper for the vocabulary sqlite-database.
	"""

	def __init__(self, path):
		"""
		Constructor.

		@param path The Path to the database file to use
		"""
		path = str(path)

		self.__connection = sqlite3.connect(path)
		self.__cursor     = self.__connection.cursor()

		self.__cursor.execute("""
			CREATE TABLE IF NOT EXISTS Vocabulary(Deutsch TEXT, Kana TEXT, Kanji TEXT, Typ TEXT, Info TEXT, Level INTEGER, Timestamp INTEGER);
			""")
		self.__connection.commit()

	def recreate(self):
		"""
		Recreate the database.

		All data will be lost.
		"""
		self.__cursor.executescript("""
			DROP TABLE IF EXISTS Vocabulary;
			CREATE TABLE Vocabulary(Deutsch TEXT, Kana TEXT, Kanji TEXT, Typ TEXT, Info TEXT, Level INTEGER, Timestamp INTEGER);
			""")
		self.__connection.commit()

	def __getTimestampNow(self):
		"""
		Get the timestamp of current time in seconds.

		@return the timestamp in seconds
		"""
		current_time = datetime.datetime.now()

		year   = current_time.year
		month  = current_time.month
		day    = current_time.day
		hour   = current_time.hour
		minute = current_time.minute
		second = current_time.second

		result = year
		result *= 12
		result += month
		result *= 31
		result += day
		result *= 24
		result += hour
		result *= 60
		result += minute
		result *= 60
		result += second

		return result

	def __getOffset(self, level):
		"""
		Get time-offset in seconds according to level of vocabulary.

		@param level vocabulary-level
		@return time-offset in seconds
		"""
		baseUnit = 24*60*60

		if level <= 0:
			return 600

		if level == 1:
			return 8*3600

		if level > 8:
			level = 8

		level -= 1

		factor = 2 ** level

		return int(baseUnit * factor)

	def __getDelta(self, level):
		"""
		Get time-delta in seconds according to level of vocabulary.

		@param level vocabulary-level
		@return time-delta in seconds
		"""

		maxDelta = int(self.__getOffset(level) / 4)

		return random.randint(-maxDelta, maxDelta)

	def __getTimestamp(self, level):
		"""
		Get timestamp in seconds when vocabulary will be asked next according to level.

		@param level vocabulary-level
		@return timestamp in seconds
		"""

		return self.__getTimestampNow() + self.__getOffset(level) + self.__getDelta(level)
	
	def commitDB(self):
		"""
		Commit the database.
		"""

		self.__connection.commit()

	def addVoc(self, data, commit=True):
		"""
		Adds vocabulary-data to the database.

		@param data vocabulary data as dictionary
		@param commit If the database-action should be committed. If set to false, commit it yourself later.
		"""

		timestamp = self.__getTimestamp(0)

		deutsch  = data['Deutsch']
		kana     = data['Kana']
		kanji    = data['Kanji']
		typ      = data['Typ']
		info     = data['Info']

		self.__cursor.execute("""
			INSERT INTO Vocabulary VALUES(?, ?, ?, ?, ?, 0, ?);
			""", (deutsch, kana, kanji, typ, info, timestamp))

		if commit:
			self.__connection.commit()
	
	def updateLevel(self, data, level):
		"""
		Update level and timestamp of given vocabulary.

		@param data vocabulary data as dictionary
		@param level the new level
		"""

		timestamp = self.__getTimestamp(level)

		deutsch   = data['Deutsch']
		kana      = data['Kana']

		self.__cursor.execute("""
			UPDATE Vocabulary SET Level=?,Timestamp=? WHERE Deutsch=? AND Kana=?;
			""", (level, timestamp, deutsch, kana))
		self.__connection.commit()
	
	def modifyVoc(self, oldData, newData):
		"""
		Modify the given vocabulary.

		@param oldData old vocabulary data
		@param newData new vocabulary data
		"""

		timestamp   = self.__getTimestamp(0)

		deutsch     = oldData['Deutsch']
		kana        = oldData['Kana']

		deutsch_new = newData['Deutsch']
		kana_new    = newData['Kana']
		kanji_new   = newData['Kanji']
		typ_new     = newData['Typ']
		info_new    = newData['Info']


		self.__cursor.execute("""
			UPDATE Vocabulary SET Deutsch=?, Kana=?, Kanji=?, Typ=?, Info=?, Level=?,Timestamp=? WHERE Deutsch=? AND Kana=?;
			""", (deutsch_new, kana_new, kanji_new, typ_new, info_new, 0, timestamp, deutsch, kana))
		self.__connection.commit()

	def deleteVoc(self, data):
		"""
		Delete the given vocabulary.

		@param data vocabulary data to delete
		"""

		deutsch = data['Deutsch']
		kana    = data['Kana']

		self.__cursor.execute("""
			DELETE FROM Vocabulary WHERE Deutsch=? AND Kana=?;
			""", (deutsch, kana))
		self.__connection.commit()

	def getNext(self):
		"""
		Get next vocabulary data.

		@return vocabulary data as dictionary
		"""

		self.__cursor.execute("""
			SELECT * FROM Vocabulary ORDER BY Timestamp;
			""")

		row = self.__cursor.fetchone()

		result = {}

		if row:
			result['Deutsch'] = row[0]
			result['Kana']    = row[1]
			result['Kanji']   = row[2]
			result['Typ']     = row[3]
			result['Info']    = row[4]
			result['Level']   = row[5]

		return result

	def resetLevel(self):
		"""
		Reset level and timestamp of all vocabulary.
		"""

		self.__cursor.execute("""
			SELECT * FROM Vocabulary ORDER BY Timestamp;
			""")

		rows = self.__cursor.fetchall()

		if rows:
			for row in rows:
				timestamp = self.__getTimestamp(0)
				deutsch   = row[0]
				kana      = row[1]
				self.__cursor.execute("""
					UPDATE Vocabulary SET Level=?,Timestamp=? WHERE Deutsch=? AND Kana=?;
					""", (0, timestamp, deutsch, kana))

		self.__connection.commit()

	def hasVoc(self, data):
		"""
		Check, if vocabulary is already in the database.

		Checks, whether there is a row in the database, where
		'Deutsch' and 'Kana' have the same value as the given data

		@param data the vocabulary data to check for
		@return True if the database contains data equal to the given data
		"""

		deutsch = data['Deutsch']
		kana    = data['Kana']

		self.__cursor.execute("""
			SELECT * FROM Vocabulary WHERE Deutsch=? AND Kana=?;
			""", (deutsch, kana))

		row = self.__cursor.fetchall()

		if len(row) > 0:
			return True
		else:
			return False
	
	def searchVoc(self, data):
		"""
		Search vocabulary similar to any key of the given data.

		@param data vocabulary data to search for
		@return an array of data dictionaries
		"""

		result = []

		for i_key in data:
			if len(data[i_key]) > 0:
				self.__cursor.execute("""
					SELECT * FROM Vocabulary WHERE %s LIKE ?;
					""" % i_key, ('%' + data[i_key] + '%',))

				rows = self.__cursor.fetchall()

				for i_row in rows:
					entry = {}

					entry['Deutsch'] = i_row[0]
					entry['Kana']    = i_row[1]
					entry['Kanji']   = i_row[2]
					entry['Typ']     = i_row[3]
					entry['Info']    = i_row[4]
					entry['Level']   = i_row[5]

					result.append(entry)

		return result

	def getTypList(self):
		"""
		Returns a list of all different 'Typ'-values of the database.

		@return all 'Typ'-values as array
		"""

		result = []

		self.__cursor.execute("""
			SELECT Typ FROM Vocabulary GROUP BY Typ;
			""")

		rows = self.__cursor.fetchall()

		for i_row in rows:
			result.append(i_row[0])

		return result

	def exportToFile(self, filename):
		"""
		Export database to a file in ';'-separated csv-format.

		Some patterns are substituted:
		- Linebreaks by '\\n'
		- Backslashes by '\\b'
		- Semicolons by '\\s'

		@param filename the name of the file to write into
		"""

		outFile = open(filename, 'w')

		self.__cursor.execute("""
			SELECT Deutsch,Kana,Kanji,Typ,Info FROM Vocabulary;
			""")

		rows = self.__cursor.fetchall()

		for i_row in rows:
			replacedLine = []
			for i_item in i_row:
				replacedLine.append(self.__exportString(i_item))

			line = ';'.join(replacedLine) + '\n'

			outFile.write(line)
	
	def importFromFile(self, filename):
		"""
		Import from a given ';'-separatedd csv-file to the database.

		Patterns that are substituted during export are resubstituted.
		Existing vocabulary with equal values in 'Deutsch' and 'Kana'
		is not replaced.

		@param filename the name  of the file to import from
		"""

		inFile = open(filename, 'r')

		for i_line in inFile:
			items = i_line.split(';')

			if len(items) < 5:
				continue
			
			data = {}

			data['Deutsch'] = self.__importString(items[0])
			data['Kana']    = self.__importString(items[1])
			data['Kanji']   = self.__importString(items[2])
			data['Typ']     = self.__importString(items[3])
			data['Info']    = self.__importString(items[4])

			if not self.hasVoc(data):
				self.addVoc(data, False)
		
		self.__connection.commit()

	def __exportString(self, string):
		"""
		Export the given string for a csv-file.

		'\\' -> '\\b'
		Linebreak -> '\\n'
		';' -> '\\s'

		@return the substituted string
		"""

		result = string.replace('\\','\\b').replace('\n','\\n').replace(';','\\s')
		return result

	def __importString(self, string):
		"""
		Import a given string from a csv-file

		'\\b' -> '\\'
		'\\n' -> Linebreak
		'\\s' -> ';'

		@return the resubstituted string
		"""

		result = string.replace('\n','').replace('\\s',';').replace('\\n','\n').replace('\\b','\\')
		return result

