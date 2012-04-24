import sqlite3
import datetime
import random

class DBVoc:

	def __init__(self, path):
		path = str(path)

		self.db_connection = sqlite3.connect(path)
		self.db_cursor     = self.db_connection.cursor()

		self.db_cursor.execute("""
			CREATE TABLE IF NOT EXISTS Vocabulary(Deutsch TEXT, Kana TEXT, Kanji TEXT, Typ TEXT, Info TEXT, Level INTEGER, Timestamp INTEGER);
			""")
		self.db_connection.commit()


	def create(self):
		self.db_cursor.executescript("""
			DROP TABLE IF EXISTS Vocabulary;
			CREATE TABLE Vocabulary(Deutsch TEXT, Kana TEXT, Kanji TEXT, Typ TEXT, Info TEXT, Level INTEGER, Timestamp INTEGER);
			""")
		self.db_connection.commit()

	def getTimestampNow(self):
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

	def getOffset(self, level):
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

	def getDelta(self, level):
		maxDelta = int(self.getOffset(level) / 4)

		return random.randint(-maxDelta, maxDelta)

	def getTimestamp(self, level):
		return self.getTimestampNow() + self.getOffset(level) + self.getDelta(level)
		
	def addVoc(self, data):
		timestamp = self.getTimestamp(0)

		deutsch = data['Deutsch']
		kana    = data['Kana']
		kanji   = data['Kanji']
		typ     = data['Typ']
		info    = data['Info']

		self.db_cursor.execute("""
			INSERT INTO Vocabulary VALUES(?, ?, ?, ?, ?, 0, ?);
			""", (deutsch, kana, kanji, typ, info, timestamp))
		self.db_connection.commit()
	
	def updateLevel(self, data, level):
		timestamp = self.getTimestamp(level)

		deutsch = data['Deutsch']
		kana    = data['Kana']

		self.db_cursor.execute("""
			UPDATE Vocabulary SET Level=?,Timestamp=? WHERE Deutsch=? AND Kana=?;
			""", (level, timestamp, deutsch, kana))
		self.db_connection.commit()
	
	def modifyVoc(self, oldData, newData):
		timestamp = self.getTimestamp(0)

		deutsch = oldData['Deutsch']
		kana    = oldData['Kana']

		deutsch_neu = newData['Deutsch']
		kana_neu    = newData['Kana']
		kanji_neu   = newData['Kanji']
		typ_neu     = newData['Typ']
		info_neu    = newData['Info']


		self.db_cursor.execute("""
			UPDATE Vocabulary SET Deutsch=?, Kana=?, Kanji=?, Typ=?, Info=?, Level=?,Timestamp=? WHERE Deutsch=? AND Kana=?;
			""", (deutsch_neu, kana_neu, kanji_neu, typ_neu, info_neu, 0, timestamp, deutsch, kana))
		self.db_connection.commit()

	def deleteVoc(self, data):
		deutsch = data['Deutsch']
		kana    = data['Kana']

		self.db_cursor.execute("""
			DELETE FROM Vocabulary WHERE Deutsch=? AND Kana=?;
			""", (deutsch, kana))
		self.db_connection.commit()

	def getNext(self):
		self.db_cursor.execute("""
			SELECT * FROM Vocabulary ORDER BY Timestamp;
			""")

		row = self.db_cursor.fetchone()

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
		self.db_cursor.execute("""
			SELECT * FROM Vocabulary ORDER BY Timestamp;
			""")

		rows = self.db_cursor.fetchall()

		if rows:
			for row in rows:
				timestamp = self.getTimestamp(0)
				deutsch   = row[0]
				kana      = row[1]
				self.db_cursor.execute("""
					UPDATE Vocabulary SET Level=?,Timestamp=? WHERE Deutsch=? AND Kana=?;
					""", (0, timestamp, deutsch, kana))

		self.db_connection.commit()

	def hasVoc(self, data):
		deutsch = data['Deutsch']
		kana    = data['Kana']

		self.db_cursor.execute("""
			SELECT * FROM Vocabulary WHERE Deutsch=? AND Kana=?;
			""", (deutsch, kana))

		row = self.db_cursor.fetchall()

		if len(row) > 0:
			return True
		else:
			return False
	
	def searchVoc(self, data):
		result = []
		for i_key in data:
			if len(data[i_key]) > 0:
				self.db_cursor.execute("""
					SELECT * FROM Vocabulary WHERE %s LIKE ?;
					""" % i_key, ('%' + data[i_key] + '%',))

				rows = self.db_cursor.fetchall()

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

	def exportToFile(self, filename):
		outFile = open(filename, 'w')

		self.db_cursor.execute("""
			SELECT Deutsch,Kana,Kanji,Typ,Info FROM Vocabulary;
			""")

		rows = self.db_cursor.fetchall()

		for i_row in rows:
			replacedLine = []
			for i_item in i_row:
				replacedLine.append(self.__exportString(i_item))

			line = ';'.join(replacedLine) + '\n'

			outFile.write(line)
	
	def importFromFile(self, filename):
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
				self.addVoc(data)


	def __exportString(self, string):
		result = string.replace('\\','\\b').replace('\n','\\n').replace(';','\\s')
		return result

	def __importString(self, string):
		result = string.replace('\\s',';').replace('\\n','\n').replace('\\b','\\')
		return result.decode('utf-8')

