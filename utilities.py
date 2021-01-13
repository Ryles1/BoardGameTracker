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
        for row in players:
            #print(row)
            print(row[1], row[2])
    else:
        print('Currently there are no players listed.')
    conn.close()

def list_games():
    query = 'SELECT * FROM games'
    conn, c = connection()
    c.execute(query)
    games = c.fetchall()
    if games:
        print('List of games:')
        for row in games:
            print(row)
    else:
        print('Currently there are no games listed.')
    conn.close()

def add_new_player():
    conn, c = connection()
    while True:
        first_name = input('Enter player first name: ').strip()
        last_name = input('Enter player last name: ').strip()
        if len(first_name.split()) > 1 or len(last_name.split()) >1:
            print('Please enter names one at a time.\n')
            continue
        elif not all([first_name, last_name, first_name.isalpha(), last_name.isalpha()]):
            print('Please enter names as alphabetical characters only.\n')
            continue
        else:
            break
    query = 'INSERT INTO players (first_name, last_name) VALUES (?,?)'
    try:
        c.execute(query, (first_name, last_name))
        conn.commit()
        conn.close()
        print(f'New player {first_name} {last_name} added successfully.')
    except sqlite3.OperationalError:
        with sqlite3.OperationalError as e:
            print(e)


def add_new_game():
    print('add_new_game')

