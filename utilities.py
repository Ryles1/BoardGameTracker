import sqlite3
from re import match


# TODO: consider rewriting this all as a "manager" class

# TODO: add a validate_name function

def connection():
    # returns connection and cursor for use with the database
    conn = sqlite3.connect('BGT.s3db')
    c = conn.cursor()
    return conn, c


def list_players():
    # query database for player info and display it to stdout
    query = 'SELECT * FROM players'
    conn, c = connection()
    c.execute(query)
    # returns list of tuples of player information - each tuple is one row from the db (one player)
    players = c.fetchall()
    if players:
        print('List of players:')
        for row in players:
            print(f'{row[0]}. {row[1]}')
    else:
        print('Currently there are no players listed.')
    conn.close()


def list_games():
    # query database for game info and display it to stdout
    query = 'SELECT * FROM games'
    conn, c = connection()
    c.execute(query)
    # returns list of tuples of game information - each tuple is one row from the db (one game)
    games = c.fetchall()
    # TODO: improve readability of game listing
    name_query = 'SELECT * from players'
    c.execute(name_query)
    # creates a dict of id:name from the name query
    names_dict = {player_row[0]: (' '.join(player_row[1:3])) for player_row in c.fetchall()}
    if games:
        print('List of games:')
        print('''ID     Date of Game    Game Played    Player     Player      Player      Player      Player      Player
              Winner''')
        # use names_dict to get actual player name for display
        for row in games:
            date = row[1]
            game = row[2]
            id_ = str(row[0])
            game_data = [
                id_,
                date,
                game,
                names_dict.get(row[3], ' - '),
                names_dict.get(row[4], ' - '),
                names_dict.get(row[5], ' - '),
                names_dict.get(row[6], ' - '),
                names_dict.get(row[7], ' - '),
                names_dict.get(row[8], ' - '),
                names_dict.get(row[9], ' - ')]
            print('\t\t'.join(game_data))
    else:
        print('Currently there are no games listed.')
    conn.close()


def edit_player():
    conn, c = connection()
    list_players()
    c.execute('Select id from players;')
    # list of all player ids as strings
    existing_players = [i[0] for i in c.fetchall()]
    while True:
        try:
            player_to_edit = int(input('Please enter the id of the player you would like to edit:  '))
        except ValueError:
            print('Please enter the player id as an integer.')
            continue
        if player_to_edit in existing_players:
            break
        else:
            print('Please enter a player from the database.')
            continue
    while True:
        # names are taken in and checked to be only alpha characters
        first_name = input('Enter player new first name: ').strip()
        last_name = input('Enter player new last name: ').strip()
        if len(first_name.split()) > 1 or len(last_name.split()) > 1:
            print('Please enter names one at a time.\n')
            continue
        elif not all([first_name, last_name, first_name.isalpha(), last_name.isalpha()]):
            print('Please enter names as alphabetical characters only.\n')
            continue
        else:
            break
    c.execute('select name from players where id = ?', (player_to_edit,))
    # returns one row from the db as a tuple
    existing_player = c.fetchone()
    name = ' '.join([first_name, last_name])
    update_query = 'UPDATE players SET name = ? where id = ?'
    print(f'Preparing to change {existing_player} to {name}.')
    confirmation = input('Enter "Yes" to confirm the update.')
    if confirmation.lower() == 'yes':
        c.execute(update_query, (name, player_to_edit))
        conn.commit()
        conn.close()
        print(f' Player id {player_to_edit} name changed to {name}.')
        return None
    else:
        print('Operation aborted.')
        return None


def edit_game():
    conn, c = connection()
    list_games()
    c.execute('Select id from games;')
    # returns list of game ids  as strings
    existing_games = [i[0] for i in c.fetchall()]
    while True:
        try:
            game_to_edit = int(input('Please enter the id of the game you would like to edit (9999 to abort):  '))
        except ValueError:
            print('Please enter the game id as an integer.')
            continue
        finally:
            if game_to_edit is None or game_to_edit not in existing_games:
                print('Please enter a game from the database.')
                continue
            elif game_to_edit == 9999:
                conn.close()
                return None
            else:
                break
    print('Please enter revised data for this game as follows: ')
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
              'please enter them into the database first (enter 9999 to quit back to menu).')
        try:
            p = int(input())
            if p == 9999:
                break
        except ValueError:
            print('Please enter only an integer for the id.\n')
            continue
        if p not in existing_players:
            print('Please enter the player in the database before adding this game.\n')
        elif p in player_ids:
            print('You have already entered that player.  Try again.\n')
        else:
            player_ids.append(str(p))
    # get the winner from user
    list_players()
    while True:
        try:
            winner = int(input('Please enter the id of the winner.  If they are not listed, '
                               'please enter them into the database first (enter 9999 to quit back to menu)'))
        except ValueError:
            print('Please enter only an integer for the id.\n')
            continue
        if winner == 9999:
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
    query = f'UPDATE games set ' \
            f'date_played = ? ' \
            f'game_played = ? ' \
            f'player1 = ?, ' \
            f'player2 = ?' \
            f'player3 = ?' \
            f'player4 = ?' \
            f'player5 = ?' \
            f'player6 = ?' \
            f'winner = ? ' \
            f'WHERE id = ?'
    # if less than 6 players participated, put null in remaining places
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
    print('Game successfully updated!')


def add_new_player():
    conn, c = connection()
    while True:
        # take in names and check they are alpha characters
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
        c.execute(query, [name])
        conn.commit()
        conn.close()
        print(f'New player {name} added successfully.')
    # try and avoid program abortion because of database errors
    except sqlite3.OperationalError:
        with sqlite3.OperationalError as e:
            print(e)


def validate_date(date):
    # date is to match format YYYY-MM-DD
    r = match(r'\d{4}-(0[1-9]|[1][12])-([0-2][0-9]|[3][0-1])', date)
    if r:
        return True
    else:
        return False


def validate_game(game):
    # game names must be alphanumeric characters and less than 50 characters long (arbitrary number)
    test_name = ''.join(game.split())
    if not test_name.isalnum():
        return False
    elif not len(game) < 50:
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
              'please enter them into the database first (enter 9999 to quit back to menu).')
        try:
            p = int(input())
            if p == 9999:
                return None
        except ValueError:
            print('Please enter only an integer for the id.\n')
            continue
        if p not in existing_players:
            print('Please enter the player in the database before adding this game.\n')
        elif p in player_ids:
            print('You have already entered that player.  Try again.\n')
        else:
            player_ids.append(str(p))
    # get the winner from user
    list_players()
    while True:
        try:
            winner = int(input('Please enter the id of the winner.  If they are not listed, '
                               'please enter them into the database first (enter 9999 to quit back to menu):\n'))
        except ValueError:
            print('Please enter only an integer for the id.\n')
            continue
        if winner == 9999:
            conn.close()
            return None
        elif winner not in existing_players:
            print('Please enter the player in the database before adding this game.\n')
            continue
        elif str(winner) not in player_ids:
            print('The winner must have played the game! Try again.\n')
            continue
        else:
            break
    query = f'INSERT INTO games (date_played, game_played, player1, player2, player3, player4, player5, player6, ' \
            f'winner) VALUES (?,?,?,?,?,?,?,?,?)'
    # if less than 6 players participated, put null in remaining places
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


def delete_games():
    conn, c = connection()
    list_games()
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
    except sqlite3.ProgrammingError:
        with sqlite3.ProgrammingError as e:
            print(e)


def delete_player():
    conn, c = connection()
    list_players()
    delete_id = int(input('Enter player id to delete: '))
    query = 'DELETE FROM players WHERE id = ?'
    confirmation = input('Enter "Yes" to delete player.')
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
    except sqlite3.ProgrammingError:
        with sqlite3.ProgrammingError as e:
            print(e)
