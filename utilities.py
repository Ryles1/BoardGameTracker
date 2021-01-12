import sqlite3

def connection():
    conn = sqlite3.connect('BGT.s3db')
    c = conn.cursor()
    return conn, c


def list_players():
    query = 'SELECT * FROM players'
    conn, c = connection()
    c.execute(query)
    players = c.fetchall()
    if players:
        print('List of players:')
        for index, row in enumerate(players):
            print(row)
    else:
        print('Currently there are no players listed.')

def list_games():
    print('list_games')

def add_new_player():
    print('add_new_player')

def add_new_game():
    print('add_new_game')

