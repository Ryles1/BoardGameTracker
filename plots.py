from matplotlib import pyplot as plt
from utilities import connection


#TODO: make a pie chart of winners
# 1. need to count wins for each player (loop each player with a database query?)
# 2. make chart with matplotlib

class PieChart():
    def __init__(self):
        self.conn, self.c = connection()
        self.players = {}

    def get_wins(self):
        c.execute('SELECT * FROM games;')
        for row in c.fetchall():
            winner = row[9]
            if self.players[winner]:
                self.players[winner] += 1
            else:
                self.players[winner] = 1

    def make_pie(self):
        pass

if __name__ == '__main__':
    chart = PieChart()
