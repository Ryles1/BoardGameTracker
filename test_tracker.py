import unittest
import sqlite3
from utilities import validate_date, validate_game

class TestCreatePlayers(unittest.TestCase):
    def test_create_players(self):
        conn = sqlite3.connect(':memory:')
        c = conn.cursor()
        c.execute('''
        CREATE TABLE if not exists players(
        id INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,
        name TEXT
        )''')
        conn.commit()
        c.close()
        c = conn.cursor()
        c.execute('INSERT INTO players (name) VALUES (?)', ['John Doe'])
        conn.commit()
        c.execute('SELECT * FROM players')
        results = c.fetchall()
        conn.close()
        self.assertEqual(1, len(results), 'Error with creating table "players"')

class TestValidateDate(unittest.TestCase):
    def test_validate_date(self):
        #test values that should pass
        true_tests = ['2020-01-01', '1990-12-31']
        true_list = list(map(validate_date, true_tests))
        #test values that should fail
        false_tests = ['89-01-01', '2020 01 01', '2020-13-01', '2020-12-32', '2020-1-01', '2020-01-1']
        false_list = list(map(validate_date, false_tests))
        self.assertNotIn(False, true_list)
        self.assertNotIn(True, false_list)

class TestValidateGame(unittest.TestCase):
    def test_validate_game(self):
        self.assertTrue(validate_game('abc'))
        self.assertFalse(validate_game('+'))
        self.assertFalse(validate_game('a'*101))

if __name__ == '__main__':
    unittest.main()