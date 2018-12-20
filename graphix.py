from codecs import open
import tatsu, sqlite3, os

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
            print "UNION"
            return "select * from (" + ast.left + " UNION " + ast.right + ")"
        elif ast.op == u'-':
            return "select * from (" + ast.left + " EXCEPT " + ast.right + ")"

    def term(self, ast):
        print "TERM " + str(ast)
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
        print "BI"
        return "select * from " + ast.i

    def listing(self, ast):
        print "LST"
        if ast == "graphs":
            return "select graph_id from graphs"

    def add(self, ast):
        if not isinstance(ast, AST):
            return ast
        else:
            return "" 
    
exists = False
if os.path.isfile("graphix.db"):
    exists = True   

grammar = open('graphix.tatsu').read()
parser = tatsu.compile(grammar)

conn = sqlite3.connect('graphix.db')
c = conn.cursor()

if not exists:
    c.executescript(sql)
    #ic.executescript(data)

class CommandLine(cmd.Cmd):
    def default(self, utterance):
        print "UTTER: " + utterance
        ast = parser.parse(utterance, semantics=QuerySemantics())
        print "AST " + str(ast)
        c.execute(ast)
        dot = Digraph()
        cnt = 0
        for row in c.fetchall():
            cnt += 1
            print str(row)
            print type(row[0])
            dot.edge(row[0].encode("ascii", "ignore"), row[1].encode("ascii", "ignore"), "")

        if cnt > 0:
            dot.render('graphix.dot', view=True)
        else:
            print "No results."

    def do_exit(self, utterance):
        return True

CommandLine().cmdloop()

