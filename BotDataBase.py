import sqlite3

DataBase = sqlite3.connect('DataBase.db')
cursor = DataBase.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS history(
    historyId INTEGER PRIMARY KEY AUTOINCREMENT,
    chatId BIGINT,
    src TEXT,
    dest TEXT,
    originalText TEXT,
    translatedText TEXT
);
''')
DataBase.commit()
DataBase.close()