import unittest
import sqlite3
from app.utilities import validate_date, validate_game

class TestCreatePlayers(unittest.TestCase):
    def test_create_players(self):
        conn = sqlite3.connect(':memory:')
        c = conn.cursor()
        c.execute('''
        CREATE TABLE if not exists players(
        id INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,
        name TEXT
        )''')
        c.execute('INSERT INTO players (name) VALUES (?)', ('John Doe'))
        c.execute('SELECT * FROM players')
        results = c.fetchall()
        conn.close()
        self.assertEqual(1, len(results), 'Error with creating table "players"')

    def test_validate_date(self):
        pass

    def test_validate_game(self):
        pass

if __name__ == '__main__':
    unittest.main()