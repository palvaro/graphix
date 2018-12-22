import unittest, tatsu, sqlite3, os
from graphix import QuerySemantics


from db import DB, sql

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

class E2ETest(unittest.TestCase):
    def setUp(self):
        grammar = open('graphix.tatsu').read()
        self.parser = tatsu.compile(grammar)
        self.db = DB("test.db")
        self.db.testdata()

    def do(self, utterance):
        print "GO " + self.parser.parse(utterance, semantics=QuerySemantics())
        return self.db.query(self.parser.parse(utterance, semantics=QuerySemantics()))

    def testAll(self):
        #results = set(self.do("1 - 3"))
        #print "results " + str(results)
        equivs = [  ("1 ^ 2", "2 ^ 1"), 
                    ("1 U 2", "2 U 1"),
                    ("(1 U 2 U 4) ^ 1", "1"),
                    ("(1 ^ 2 ^ 4)", "4 ^ 1 ^ 2"),
        ]

        for l,r in equivs:
            print l + " vs " + r
            self.assertEqual(set(self.do(l)), set(self.do(r)))

    def testTest(self):
        #for row in self.do("1 - 3"):
        #    print str(row)
        self.assertEqual(set(self.do("1-3")), set([(u'C', u'D')]))


if __name__ == '__main__':
    unittest.main()
