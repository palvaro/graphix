from codecs import open
import tatsu, sqlite3, os, hashlib
from db import DB

import cmd

from tatsu.ast import AST
from pprint import pprint
from graphviz import Digraph

sql="""
create table graphs (
    graph_id int,
    graph_class int,
    status int
);

create table nodes (
    graph_id int,
    node_id int,
    name varchar(255)
);

create table edges (
    from_node int,
    to_node int,
    label varchar(255)
);

create view logical as
select from_x.graph_id, from_x.name from_n, to_x.name to_n
     from nodes from_x, nodes to_x, edges e
        where from_x.node_id = e.from_node
        and to_x.node_id = e.to_node;
"""


class QuerySemantics(object):
    def barenumber(self, ast):
        return "select from_n, to_n from logical where graph_id = " + ast.n

    def expr(self, ast):
        if not isinstance(ast, AST):
            return ast
        elif ast.op == u'^':
            return "select * from (" + ast.left + " INTERSECT " + ast.right + ")"
        elif ast.op == u'U':
            return "select * from (" + ast.left + " UNION " + ast.right + ")"
        elif ast.op == u'-':
            return "select * from (" + ast.left + " EXCEPT " + ast.right + ")"

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
        if os.path.isfile("Graphix.db"):
            self.db = DB("Graphix.db", False)
        else:
            self.db = DB("Graphix.db")

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

