from codecs import open
import tatsu, sqlite3, os, hashlib
from db import DB

import cmd

from tatsu.ast import AST
from pprint import pprint
from graphviz import Digraph

class QuerySemantics(object):
    def barenumber(self, ast):
        return "select from_n, to_n from logical where graph_id = " + ast.n

    def expr2(self, ast):
        if not isinstance(ast, AST):
            return ast
        elif ast.op == u'^':
            return "select * from (" + ast.left + " INTERSECT " + ast.right + ")"
        elif ast.op == u'U':
            return "select * from (" + ast.left + " UNION " + ast.right + ")"
        elif ast.op == u'-':
            return "select * from (" + ast.left + " EXCEPT " + ast.right + ")"

    def expr(self, ast):
        return ast.e

    def intersect(self, ast):
        if not isinstance(ast, AST):
            return ast
        else:
            return "select * from (" + ast.left + " INTERSECT " + ast.right + ")"

    def union(self, ast):
        if not isinstance(ast, AST):
            return ast
        else:
            return "select * from (" + ast.left + " UNION " + ast.right + ")"

    def minus(self, ast):
        if not isinstance(ast, AST):
            return ast
        else:
            #return "select * from (" + ast.left + " EXCEPT " + ast.right + ")"
            rhs1 = "select from_n from (" + ast.right + ")"
            rhs2 = "select to_n from (" + ast.right + ")"
            uni = rhs1 + " UNION " + rhs2 
            return "select * from (select * from (" + ast.left + ") where from_n not in (" + uni + ") and to_n not in (" + uni + ") EXCEPT " + ast.right + ")"


    def term(self, ast):
        if not isinstance(ast, AST):
            return ast
        else:
            return ast.t

    def assn(self, ast):
        if not isinstance(ast, AST):
            return ast
        else:
            return "CREATE VIEW " + ast.name + " AS " + ast.e

    def bareident(self, ast):
        return "select * from " + ast.i

    def listing(self, ast):
        if ast == "graphs":
            return "select graph_id from graphs"

    def add(self, ast):
        if not isinstance(ast, AST):
            return ast
        else:
            return "" 

    

class CommandLine(cmd.Cmd):
    def __init__(self, logging=False):
        cmd.Cmd.__init__(self)
        self.logging = logging
        if logging:
            self.logfp = open("log.html", "w")
        if os.path.isfile("graphix.db"):
            self.db = DB("graphix.db", False)
        else:
            self.db = DB("graphix.db")

        grammar = open('graphix.tatsu').read()
        self.parser = tatsu.compile(grammar)

    def default(self, utterance):
        ast = self.parser.parse(utterance, semantics=QuerySemantics())
        print "AST " + str(ast)
        #c.execute(ast)
        dot = Digraph(format='png')
        cnt = 0
        #for row in c.fetchall():
        for row in self.db.query(ast):
            cnt += 1
            #print str(row)
            dot.edge(row[0].encode("ascii", "ignore"), row[1].encode("ascii", "ignore"), "")

        if cnt > 0:
            dot.render('graphix.dot', view=True)
        else:
            print "No results."

        if self.logging:
            name = hashlib.md5(utterance).hexdigest()
            fn = 'graphix.' + name + '.dot'
            dot.render(fn, "img")
            self.logfp.write("<br>")
            self.logfp.write("Expression: <b><h3>" + utterance  + "</b></h3>")
            self.logfp.write("<br>")
            self.logfp.write("<img src = \"img/graphix." + name + ".dot.png\">")
            self.logfp.write("<hr>")
            
            

    def do_exit(self, utterance):
        if self.logging:
            self.logfp.close()
        return True

if __name__ == '__main__':
    CommandLine(True).cmdloop()

