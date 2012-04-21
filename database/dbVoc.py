import sqlite3
import datetime
import random

class DBVoc:

	def __init__(self, path):
		path = str(path)

		self.db_connection = sqlite3.connect(path)
		self.db_cursor     = self.db_connection.cursor()

	def create(self):
		self.db_cursor.executescript("""
			DROP TABLE IF EXISTS Vocabulary;
			CREATE TABLE Vocabulary(Deutsch TEXT, Kana TEXT, Kanji TEXT, Typ TEXT, Info TEXT, Level INTEGER, Timestamp INTEGER);
			""")
		self.db_connection.commit()

	def getTimestamp(self, level):
		level = int(level)

		current_time = datetime.datetime.now()

		year   = current_time.year
		month  = current_time.month
		day    = current_time.day
		hour   = current_time.hour
		minute = current_time.minute
		second = current_time.second

		if level <= 0:
			minute += random.randint(-100,100)
			second += random.randint(-60, 60)
		elif level == 1:
			hour   += 2
			minute += random.randint(-60,60) 
			second += random.randint(-60,60)
		elif level == 2:
			hour   += 12 
			hour   += random.randint(-6,6) 
			minute += random.randint(-60,60) 
			second += random.randint(-60,60)
		elif level == 3:
			day    += 2
			hour   += random.randint(-24,24) 
			minute += random.randint(-60,60) 
			second += random.randint(-60,60)
		elif level == 4:
			day    += 6
			day    += random.randint(-2,2)
			hour   += random.randint(-24,24) 
			minute += random.randint(-60,60) 
			second += random.randint(-60,60)
		else:
			day    += 14
			day    += random.randint(-5,5)
			hour   += random.randint(-24,24) 
			minute += random.randint(-60,60) 
			second += random.randint(-60,60)
		
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

	
	def addVoc(self, deutsch, kana, kanji, typ, info):
		timestamp = self.getTimestamp(0)
		self.db_cursor.execute("""
			INSERT INTO Vocabulary VALUES(?, ?, ?, ?, ?, 0, ?);
			""", (deutsch, kana, kanji, typ, info, timestamp))
		self.db_connection.commit()
	
	def updateLevel(self, deutsch, kana, level):
		timestamp = self.getTimestamp(level)
		self.db_cursor.execute("""
			UPDATE Vocabulary SET Level=?,Timestamp=? WHERE Deutsch=? AND Kana=?;
			""", (level, timestamp, deutsch, kana))
		self.db_connection.commit()
	
	def modifyVoc(self, deutsch, kana, deutsch_neu, kana_neu, kanji_neu, typ_neu, info_neu):
		timestamp = self.getTimestamp(0)
		self.db_cursor.execute("""
			UPDATE Vocabulary SET Deutsch=?, Kana=?, Kanji=?, Typ=?, Info=?, Level=?,Timestamp=? WHERE Deutsch=? AND Kana=?;
			""", (deutsch_neu, kana_neu, kanji_neu, typ_neu, info_neu, 0, timestamp, deutsch, kana))
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

	def hasVoc(self, deutsch, kana):
		self.db_cursor.execute("""
			SELECT * FROM Vocabulary WHERE Deutsch=? AND Kana=?;
			""", (deutsch, kana))

		row = self.db_cursor.fetchall()

		if len(row) > 0:
			return True
		else:
			return False
