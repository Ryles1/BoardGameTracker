import sqlite3
from utilities import connection

def create_games():
    create_games_query = '''
    CREATE TABLE if not exists games(
    id INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,
    date_played TEXT,
    game_played TEXT,
    FOREIGN KEY (id) REFERENCES players (id),
    FOREIGN KEY (id) REFERENCES players (id),
    FOREIGN KEY (id) REFERENCES players (id),
    FOREIGN KEY (id) REFERENCES players (id),
    FOREIGN KEY (id) REFERENCES players (id),
    FOREIGN KEY (id) REFERENCES players (id),
    FOREIGN KEY (id) REFERENCES players (id)
    )'''
    conn, c = connection()
    c.execute(create_games_query)
    conn.commit()
    conn.close()

def create_players():
    create_players_query = '''
        CREATE TABLE if not exists players(
        id INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,
        first_name TEXT,
        last_name TEXT
        )'''
    conn, c = connection()
    c.execute(create_players_query)
    conn.commit()
    conn.close()

def create_tables():
    pass