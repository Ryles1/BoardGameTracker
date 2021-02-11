from matplotlib import pyplot as plt
from utilities import connection


class GlobalPieChart:
    def __init__(self):
        self.players = {}
        self.get_wins()

    def get_wins(self):
        conn, cursor = connection()
        cursor.execute('SELECT * FROM games;')
        rows = cursor.fetchall()
        cursor.execute('SELECT * FROM players')
        name_dict = {row[0]:row[1] for row in cursor.fetchall()}
        for row in rows:
            winner_id = row[9]
            winner = name_dict.get(winner_id, 'Not Found')
            if self.players.get(winner):
                self.players[winner] += 1
            else:
                self.players[winner] = 1

    def make_pie(self):
        # make a pie chart of each players wins
        wins = self.players.values()
        names = self.players.keys()
        fig, ax = plt.subplots()
        # autopct is calculated in order to show the integer number of wins instead of the percentage
        wedges, texts, autotexts = ax.pie(wins, autopct=lambda x: f'{x/100*sum(wins):.0f}', labels=names,
                                          textprops=dict(color='w'), radius=0.8)
        ax.axis('equal')
        ax.set_title('Board Game Wins by Player')
        plt.legend(wedges, names, loc='upper right', bbox_to_anchor=(1.1, 1))
        fig.tight_layout()
        plt.style.use('ggplot')
        plt.show()


class IndividualChart:
    def __init__(self, player):
        self.player = player
        self.games = {}

    def get_games(self):
        conn, cursor = connection()
        #get player id
        cursor.execute('SELECT id FROM players WHERE name=?', (self.player,))
        id = cursor.fetchone()[0]
        # get game name for all games played and put them in a dict as keys
        cursor.execute('SELECT game_played from games;')
        self.games = {row[0]: {'played': 0, 'wins': 0} for row in cursor.fetchall()}
        # for each game that has been played, count the wins and put them in the dict
        for game in self.games.keys():
            cursor.execute('SELECT count(*) FROM games WHERE game_played = ? and winner = ?;', (game, id))
            game_wins = cursor.fetchone()[0]
            self.games[game]['wins'] = game_wins
        for game in self.games.keys():
            cursor.execute('SELECT count(*) FROM games WHERE game_played = ? and '
                           '(player1 = ? or player2 = ? or player3 = ? or player4 = ?'
                           'or player5 = ? or player6 = ?)', [game]+[id]*6)
            games_played = cursor.fetchone()[0]
            self.games[game]['played'] = games_played

    def make_chart(self):
        played = [i['played'] for i in self.games.values()]
        won = [j['wins'] for j in self.games.values()]
        # stacked bar chart of games with number of games played and won
        fig, ax = plt.subplots()
        width = 0.3
        rect1 = ax.bar(self.games.keys(), won, width, align='edge', label='Games Played')
        rect2 = ax.bar(self.games.keys(), played, (width * -1), align='edge', label='Games Won')
        ax.set_ylabel('Games')
        ax.set_title(f'Games Played and Won ({self.player})')
        plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right')
        ax.legend()
        fig.tight_layout()
        plt.show()


