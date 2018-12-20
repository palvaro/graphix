from codecs import open
import tatsu, sqlite3, os

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

data="""
insert into graphs values (1, 1, 0);
insert into nodes values (1, 1, "A");
insert into nodes values (1, 2, "B");
insert into nodes values (1, 3, "C");
insert into edges values (1, 2, NULL);
insert into edges values (1, 3, NULL);

insert into graphs values (2, 1, 0);
insert into nodes values (2, 4, "A");
insert into nodes values (2, 5, "B");
insert into nodes values (2, 6, "C");
insert into edges values (4, 5, NULL);
insert into edges values (4, 6, NULL);
insert into nodes values (2, 7, "D");
insert into edges values  (6, 7, NULL);


insert into graphs values(3, 1, 1);
insert into nodes values (3, 8, "A");
insert into nodes values (3, 9, "B");
insert into nodes values (3, 10, "X");

insert into edges values (8, 9, NULL);
insert into edges values (8, 10, NULL);

"""

class QuerySemantics(object):
    def number(self, ast):
        return "select from_n, to_n from logical where graph_id = " + ast 

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
    
try:    
    os.remove("graphix.db")
except:
    pass

    

grammar = open('graphix.tatsu').read()
parser = tatsu.compile(grammar)

#ast = parser.parse("((0 ^ 1 ^ 2 ^ 3) U (7 ^ 8)) - 5", semantics=QuerySemantics())
#pprint(ast, width=20, indent=4)
#ast = parser.parse("(0 - 1)", semantics=QuerySemantics())
#pprint(ast, width=20, indent=4)


conn = sqlite3.connect('graphix.db')
c = conn.cursor()

c.executescript(sql)
c.executescript(data)
while True:
    q = raw_input("Query: ")
    ast = parser.parse(q, semantics=QuerySemantics())
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

