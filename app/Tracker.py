import tables
import utilities
from sys import exit

# 1. make a database with tables for players, games, and association table between the two COMPLETE
# 2. need functions to add players, and add games with associated information COMPLETE
# 3. need functino to display list of games, players COMPLETE
# 3a. make some plots and statistics?
# 3b. functions for updating player/game data?
# 4. add a GUI?
# 5. make a web app?
def menu():
    print('''
    1. List Players
    2. List Games
    3. Add new player
    4. Add new game
    5. Quit
    Please make a selection.
    ''')
    while True:
        try:
            user_choice = int(input())
            if user_choice in list(range(1,7)):
                return user_choice
            else:
                print('Enter a number between 1 and 5.')
                continue
        except ValueError:
            print('Enter a number between 1 and 5.')
            continue


def main():
    #1. check if database and tables exist
    tables.create_games()
    tables.create_players()
    #2. Main menu loop
    while True:
        user_choice = menu()
        if user_choice == 5:
            print('Bye!')
            exit()
        elif user_choice == 6:
            utilities.delete_games()
        elif user_choice == 1:
            utilities.list_players()
        elif user_choice == 2:
            utilities.list_games()
        elif user_choice == 3:
            utilities.add_new_player()
        elif user_choice == 4:
            utilities.add_new_game()
        else:
            pass


if __name__ == '__main__':
    main()
