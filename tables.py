from utilities import connection

def create_games():
    create_games_query = '''
    CREATE TABLE if not exists games(
    id INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,
    date_played TEXT,
    game_played TEXT,
    player1 TEXT,
    player2 TEXT,
    player3 TEXT,
    player4 TEXT,
    player5 TEXT,
    player6 TEXT,
    winner TEXT,
    FOREIGN KEY (player1) REFERENCES players (id),
    FOREIGN KEY (player2) REFERENCES players (id),
    FOREIGN KEY (player3) REFERENCES players (id),
    FOREIGN KEY (player4) REFERENCES players (id),
    FOREIGN KEY (player5) REFERENCES players (id),
    FOREIGN KEY (player6) REFERENCES players (id),
    FOREIGN KEY (winner) REFERENCES players (id)
    )'''
    conn, c = connection()
    c.execute(create_games_query)
    conn.commit()
    conn.close()

def create_players():
    create_players_query = '''
        CREATE TABLE if not exists players(
        id INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,
        name TEXT
        )'''
    conn, c = connection()
    c.execute(create_players_query)
    conn.commit()
    conn.close()
