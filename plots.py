from matplotlib import pyplot as plt
from utilities import connection


class GlobalPieChart:
    def __init__(self):
        self.players = {}
        self.get_wins()

    def get_wins(self):
        conn, cursor = connection()
        cursor.execute('SELECT * FROM games;')
        for row in cursor.fetchall():
            winner = row[9]
            if self.players.get(winner):
                self.players[winner] += 1
            else:
                self.players[winner] = 1

    def make_pie(self):
        wins = self.players.values()
        names = self.players.keys()
        fig, ax = plt.subplots()
        ax.pie(wins, labels=names, shadow=True)
        ax.axis('equal')
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
            cursor.execute('SELECT count(*) FROM games WHERE player1 = ? or player2 = ? or player3 = ? or player4 = ?'
                           'or player5 = ? or player6 = ?', [id]*6)
            game_played = cursor.fetchone()[0]
            self.games[game]['played'] = game_played

    def make_chart(self):
        pass

