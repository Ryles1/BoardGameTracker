from matplotlib import pyplot as plt
from utilities import connection


class GlobalPieChart:
    def __init__(self):
        self.conn, self.c = connection()
        self.players = {}
        self.get_wins()

    def get_wins(self):
        self.c.execute('SELECT * FROM games;')
        for row in self.c.fetchall():
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
