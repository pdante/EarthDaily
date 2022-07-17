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

    def getAllBirds(self, n, s, e, w):
        sql = """
            SELECT bird_id 
            FROM Birds
            WHERE lat <= ? AND lat >= ?
                AND ((?>=? AND lng<=? AND lng>=?) OR (lng<=? OR lng >= ?)"""
        params = (n, s, e, w, e, w, e, w)
        ids = self.cur.execute(sql, params)
        sql = """
            SELECT b.bird_name AS 'Name'
                , b.lat AS 'Latitude'
                , b.lng AS 'Longitude'
                , d.year || d.month || d.day AS 'Day'
            FROM Birds AS b 
            LEFT JOIN Dates AS d ON b.date_id = d.date_id
            WHERE b.bird_id IN ?
                """
        params = (ids,)

        return self.cur.execute(sql, params)

    def getAllBirdsDay(self, n, s, e, w, day, month, year):
        sql = """
                SELECT bird_id 
                FROM Birds
                WHERE lat <= ? AND lat >= ?
                    AND ((?>=? AND lng<=? AND lng>=?) OR (lng<=? OR lng >= ?)
                    AND year = ? AND month = ? AND day = ?"""
        params = (n, s, e, w, e, w, e, w, year, month, day)
        ids = self.cur.execute(sql, params)
        sql = """
                SELECT b.bird_name AS 'Name'
                    , b.lat AS 'Latitude'
                    , b.lng AS 'Longitude'
                    , d.year || d.month || d.day AS 'Day'
                FROM Birds AS b 
                LEFT JOIN Dates AS d ON b.date_id = d.date_id
                    WHERE b.bird_id IN ?
                        """
        params = (ids,)

        return self.cur.execute(sql, params)

    def getBirds(self, n, s, e, w, name):
        sql = """
                    SELECT bird_id 
                    FROM Birds
                    WHERE name like ?
                        AND lat <= ? AND lat >= ?
                        AND ((?>=? AND lng<=? AND lng>=?) OR (lng<=? OR lng >= ?)"""
        params = (name.capitalize(), n, s, e, w, e, w, e, w)
        ids = self.cur.execute(sql, params)
        sql = """
                    SELECT b.bird_name AS 'Name'
                        , b.lat AS 'Latitude'
                        , b.lng AS 'Longitude'
                        , d.year || d.month || d.day AS 'Day'
                    FROM Birds AS b 
                    LEFT JOIN Dates AS d ON b.date_id = d.date_id
                    WHERE b.bird_id IN ?
                """
        params = (ids,)

        return self.cur.execute(sql, params).fetchall()

    def getBirdsDay(self, n, s, e, w, name, day, month, year):
        sql = """
                            SELECT bird_id 
                            FROM Birds
                            WHERE name like ?
                                AND lat <= ? AND lat >= ?
                                AND ((?>=? AND lng<=? AND lng>=?) OR (lng<=? OR lng >= ?)
                                AND year = ? AND month = ? AND day = ?"""
        params = (name.capitalize(), n, s, e, w, e, w, e, w, year, month, day)
        ids = self.cur.execute(sql, params)
        sql = """
                            SELECT b.bird_name AS 'Name'
                                , b.lat AS 'Latitude'
                                , b.lng AS 'Longitude'
                                , d.year || d.month || d.day AS 'Day'
                            FROM Birds AS b 
                            LEFT JOIN Dates AS d ON b.date_id = d.date_id
                            WHERE b.bird_id IN ?
                        """
        params = (ids,)

        return self.cur.execute(sql, params).fetchall()

    def createBird(self, name, lat, lng, day, month, year):
        pass

    def getDateId(self, day, month, year):
        pass


d = DBInterface()
d.setup()
