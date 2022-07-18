import sqlite3


class DBInterface:
    def __init__(self):
        self.dbname = 'data/birddb.db'
        self.con = sqlite3.connect(self.dbname, check_same_thread=False)
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
        cur = self.con.cursor()
        cap_name = name.capitalize()
        date_id = self.getDateId(day, month, year)
        sql = """select bird_id from Birds where bird_name like ? AND lat = ? AND lng = ? and date_id = ?"""
        params = (cap_name, lat, lng, date_id)
        row = cur.execute(sql, params).fetchone()
        if not row:
            sql = """INSERT INTO Birds (bird_name, lat, lng, date_id) VALUES(?,?,?,?)"""
            cur.execute(sql, params)
            sql = """select * from Birds"""
            rows = self.cur.execute(sql, ).fetchall()
            self.con.commit()
            cur.close()
            return "You added a new bird to the database"
        else:
            cur.close()
            return "There is already a bird recorded with that name, at that location, on that day"

    def deleteBird(self, name, lat, lng, day, month, year):
        cur = self.con.cursor()
        cap_name = name.capitalize()
        date_id = self.getDateId(day, month, year)
        sql = """DELETE FROM Birds
                    WHERE bird_name = ? AND lat = ? AND lng = ? and date_id = ?"""
        params = (cap_name,lat,lng,date_id)
        cur.execute(sql,params)
        self.con.commit()
        cur.close()

    def getDateId(self, day, month, year):
        cur = self.con.cursor()
        sql = """select date_id from Dates where day = ? and month = ? and year = ?"""
        params = (day, month, year)
        row = cur.execute(sql, params).fetchone()
        if row:
            d_id = row['date_id']
            cur.close()
            return d_id
        else:
            sql = """INSERT INTO Dates (day, month, year) VALUES(?,?,?) RETURNING date_id"""
            row = cur.execute(sql, params).fetchone()
            self.con.commit()
            cur.close()
            return row['date_id']


d = DBInterface()
d.setup()
