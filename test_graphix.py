import unittest, tatsu, sqlite3, os


from graphix import sql
from db import DB

class TestDB(unittest.TestCase):
    def testDB(self):
        db = DB("foo.db")
        assert(os.path.isfile("foo.db"))

        db2 = DB("foo.db", False)
        os.remove("foo.db")

    def testDB2(self):
        with self.assertRaises(Exception):
            DB("bar", False)

    def testQuery(self):
        db = DB("test.db")
        db.testdata()
        cnt = 0
        for row in db.query("select * from logical"):
            cnt += 1
        self.assertEqual(cnt, 12)

    
        
        

class TestGraphix(unittest.TestCase):
    def setUp(self):
        grammar = open('graphix.tatsu').read()
        #self.parser = tatsu.compile(grammar)
        #self.conn = sqlite3.connect('test.db')
        #self.c = self.conn.cursor()

        #self.c.executescript(sql)
 

    def testOne(self):
        print "OK"



    #def tearDown(self):
    #    os.remove("test.db")


if __name__ == '__main__':
    unittest.main()
