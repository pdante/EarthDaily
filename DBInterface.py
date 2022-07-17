import sqlite3

class DBInterface:
    def __init__(self):
        self.con = sqlite3.connect('data/birddb.db')
        self.con.row_factory = sqlite3.Row
        self.cur = self.con.cursor()
        