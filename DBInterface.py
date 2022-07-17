import sqlite3


class DBInterface:
    def __init__(self):
        self.con = sqlite3.connect('data/birddb.db')
        self.con.row_factory = sqlite3.Row
        self.cur = self.con.cursor()

    def setup(self):
        pathToSql = 'sql/birdsql.sql'
        with open(pathToSql, 'r') as scriptfile:
            contents = scriptfile.read()
            self.cur.executescript(contents)

    def getBirds(self,name, n, s, e, w):
        pass

    def getBirdsNoName(self,n,s,e,w):
        pass

    def createBird(self, name, lat, lng, start_hour, end_hour, day, month, year):
        pass

    def getDateId(self, day, month, year):
        pass

    def getTimeId(self, start, end):
        pass


d = DBInterface()
d.setup()