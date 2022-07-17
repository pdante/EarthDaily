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

    def getAllBirds(self,n,s,e,w):
        pass


    def getAllBirdsDay(self, n, s, e, w, day, month, year):
        pass


    def getBirds(self,n,s,e,w, name):
        pass


    def getBirdsDay(self,n,s,e,w, name, day, month, year):
        pass


    def createBird(self, name, lat, lng, day, month, year):
        pass

    def getDateId(self, day, month, year):
        pass



d = DBInterface()
d.setup()