import sqlite3
from re import match


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
            # print(row)
            print(f'{row[0]}. {row[1]} {row[2]}')
    else:
        print('Currently there are no players listed.')
    conn.close()


def list_games():
    query = 'SELECT * FROM games'
    conn, c = connection()
    c.execute(query)
    games = c.fetchall()
    # TODO: improve readability of game listing
    name_query = 'SELECT * from players'
    c.execute(name_query)
    names_dict = {player_row[0]: (' '.join(player_row[1:3])) for player_row in c.fetchall()}
    if games:
        print('List of games:')
        print('''Date of Game    Game Played    Player     Player      Player      Player      Player      Player      Winner''')
        for row in games:
            game_data = [
            row[1],
            row[2],
            names_dict.get(row[3],' - '),
            names_dict.get(row[4],' - '),
            names_dict.get(row[5],' - '),
            names_dict.get(row[6],' - '),
            names_dict.get(row[7],' - '),
            names_dict.get(row[8],' - '),
            names_dict.get(row[9],' - ')]
            print('\t\t'.join(game_data))
    else:
        print('Currently there are no games listed.')
    conn.close()


def add_new_player():
    conn, c = connection()
    while True:
        first_name = input('Enter player first name: ').strip()
        last_name = input('Enter player last name: ').strip()
        if len(first_name.split()) > 1 or len(last_name.split()) > 1:
            print('Please enter names one at a time.\n')
            continue
        elif not all([first_name, last_name, first_name.isalpha(), last_name.isalpha()]):
            print('Please enter names as alphabetical characters only.\n')
            continue
        else:
            break
    name = ' '.join([first_name, last_name])
    query = 'INSERT INTO players (name) VALUES (?)'
    try:
        c.execute(query, name)
        conn.commit()
        conn.close()
        print(f'New player {name} added successfully.')
    except sqlite3.OperationalError:
        with sqlite3.OperationalError as e:
            print(e)


def validate_date(date):
    r = match(r'\d{4}-(0[1-9]|[1][12])-([0-2][0-9]|[3][0-1])', date)
    if r:
        return True
    else:
        return False


def validate_game(game):
    test_name = ''.join(game.split())
    if not test_name.isalnum():
        return False
    elif not len(game) < 100:
        return False
    else:
        return True


def add_new_game():
    conn, c = connection()
    # while loop for getting name of game and date played
    while True:
        game_played = input('Enter game: ').strip().title()
        # split and re-join game by words in case there are extra spaces
        game_played = ' '.join(game_played.split())
        date_played = input('Enter date of game (format YYYY-MM-DD): ').strip()
        date_ok = validate_date(date_played)
        game_ok = validate_game(game_played)
        if date_ok:
            if game_ok:
                break
            else:
                print('There was an error with the game name, please try again:')
                continue
        else:
            print('There was an error with the date, please try again (format YYYY-MM-DD):')
            continue

    while True:
        try:
            num_players = int(input('Enter the number of players (2 - 6): '))
        except ValueError:
            print('Please enter an integer number of players between 2 and 6.')
            continue
        finally:
            if not 2 <= num_players <= 6:
                print('Please enter an integer number of players between 2 and 6.')
                continue
            else:
                break
    player_ids = []
    # print list of players, get player ids, validate they are in database already
    list_players()
    c.execute('Select id from players;')
    existing_players = [i[0] for i in c.fetchall()]
    # while loop for getting names of players
    while len(player_ids) != num_players:
        print('Please enter the id of the player.  If they are not listed, '
              'please enter them into the database first (enter 100 to quit back to menu).')
        try:
            p = int(input())
            if p == 100:
                break
        except ValueError:
            print('Please enter only an integer for the id.\n')
            continue
        if p not in existing_players:
            print('Please enter the player in the database before adding this game.\n')
        elif p in player_ids:
            print('You have already entered that player.  Try again.\n')
        else:
            player_ids.append(p)
    # get the winner from user
    list_players()
    while True:
        try:
            winner = int(input('Please enter the id of the winner.  If they are not listed, '
                               'please enter them into the database first (enter 100 to quit back to menu)'))
        except ValueError:
            print('Please enter only an integer for the id.\n')
            continue
        if winner == 100:
            conn.close()
            return None
        elif winner not in existing_players:
            print('Please enter the player in the database before adding this game.\n')
            continue
        elif winner not in player_ids:
            print('The winner must have played the game! Try again.\n')
            continue
        else:
            break
    query = f'INSERT INTO games (date_played, game_played, player1, player2, player3, player4, player5, player6, ' \
            f'winner) VALUES (?,?,?,?,?,?,?,?,?)'
    nulls = ['NULL' for _ in range(6 - len(player_ids))]
    player_ids = player_ids + nulls
    values = (date_played,
              game_played,
              player_ids[0],
              player_ids[1],
              player_ids[2],
              player_ids[3],
              player_ids[4],
              player_ids[5],
              winner,
              )
    c.execute(query, values)
    conn.commit()
    conn.close()
    print('Game successfully added!')
    # print(player_ids, values, query, sep='\n')


def delete_games():
    conn, c = connection()
    delete_id = int(input('Enter game id to delete '))
    query = 'DELETE FROM games WHERE id = ?'
    confirmation = input('Enter "Yes" to delete game.')
    if confirmation != 'Yes':
        print('Delete operation aborted')
        return None
    try:
        c.execute(query, (delete_id,))
        conn.commit()
        conn.close()
    except sqlite3.OperationalError:
        with sqlite3.OperationalError as e:
            print(e)
