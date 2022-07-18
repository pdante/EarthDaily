import unittest
from DBInterface import DBInterface as DB


class MyTestCase(unittest.TestCase):
    def test_createBird(self):
        db = DB()
        db.deleteBird("Sparrow", 75.23, -80.112, 1, 2, 1000)
        db.deleteBird("Sparrow", 75.23, -80.112, 2, 2, 1000)
        db.deleteBird("Hawk", 75.23, -80.112, 1, 2, 1000)
        db.deleteBird("Hawk", 74.23, -80.112, 1, 2, 1000)
        self.assertEqual(db.createBird("Sparrow", 75.23, -80.112, 1, 2, 1000), "You added a new bird to the database")
        self.assertEqual(db.createBird("Sparrow", 75.23, -80.112, 1, 2, 1000), "There is already a bird recorded with that name, at that location, on that day")
        db.deleteBird("Sparrow", 75.23, -80.112, 1, 2, 1000)
        self.assertEqual(db.createBird("Sparrow", 75.23, -80.112, 1, 2, 1000), "You added a new bird to the database")
        self.assertEqual(db.createBird("Sparrow", 75.23, -80.112, 2, 2, 1000), "You added a new bird to the database")
        self.assertEqual(db.createBird("Hawk", 75.23, -80.112, 1, 2, 1000), "You added a new bird to the database")
        self.assertEqual(db.createBird("Hawk", 74.23, -80.112, 1, 2, 1000), "You added a new bird to the database")
        db.deleteBird("Sparrow", 75.23, -80.112, 1, 2, 1000)
        db.deleteBird("Sparrow", 75.23, -80.112, 2, 2, 1000)
        db.deleteBird("Hawk", 75.23, -80.112, 1, 2, 1000)
        db.deleteBird("Hawk", 74.23, -80.112, 1, 2, 1000)

    def test_capitalizing(self):
        db = DB()
        db.deleteBird("Sparrow", 75.23, -80.112, 1, 2, 1000)
        self.assertEqual(db.createBird("Sparrow", 75.23, -80.112, 1, 2, 1000), "You added a new bird to the database")
        self.assertEqual(db.createBird("spaRrow", 75.23, -80.112, 1, 2, 1000),"There is already a bird recorded with that name, at that location, on that day")
        db.deleteBird("Sparrow", 75.23, -80.112, 1, 2, 1000)

if __name__ == '__main__':
    unittest.main()
