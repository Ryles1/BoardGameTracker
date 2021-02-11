import tables
import utilities
from sys import exit
from plots import GlobalPieChart, IndividualChart

# 1. make a database with tables for players, games, and association table between the two COMPLETE
# 2. need functions to add players, and add games with associated information COMPLETE
# 3. need functino to display list of games, players COMPLETE
# 3a. make some plots and statistics? COMPLETE PIE CHART
# 3b. functions for updating player/game data? COMPLETE
# 3c. add tests TESTS ADDED FOR SOME UTILITIES
# 4. add a GUI?
# 4a. make an executable?
# 5. make a web app?


def menu():
    print('''
    0. Quit
    1. List players
    2. List games
    3. Add new player
    4. Add new game
    5. Edit player
    6. Edit game
    7. View global win record
    8. View individual win record
    9. Delete player
    10. Delete game 
    Please make a selection.
    ''')
    while True:
        try:
            user_choice = int(input())
            if user_choice in list(range(0, 11)):
                return user_choice
            else:
                print('Enter a number between 0 and 10.')
                continue
        except ValueError:
            print('Enter a number between 0 and 10.')
            continue


def main():
    # 1. check if database and tables exist
    tables.create_games()
    tables.create_players()
    # 2. Main menu loop
    while True:
        user_choice = menu()
        if user_choice == 0:
            print('Bye!')
            exit()
        elif user_choice == 9:
            utilities.delete_player()
        elif user_choice == 10:
            utilities.delete_games()
        elif user_choice == 1:
            utilities.list_players()
        elif user_choice == 2:
            utilities.list_games()
        elif user_choice == 3:
            utilities.add_new_player()
        elif user_choice == 4:
            utilities.add_new_game()
        elif user_choice == 5:
            utilities.edit_player()
        elif user_choice == 6:
            utilities.edit_game()
        elif user_choice == 7:
            pie = GlobalPieChart()
            pie.make_pie()
        elif user_choice == 8:
            player = input('Enter name of desired player: ')
            pie = IndividualChart(player)
            pie.get_games()
            pie.make_chart()
        else:
            pass


if __name__ == '__main__':
    main()
