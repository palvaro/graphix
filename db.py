import sqlite3, os

from test_data import test_data

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


class DB():
    def __init__(self, fn=None, fresh=True):
        if fresh:
            if fn is not None and os.path.isfile(fn):
                os.remove(fn)
        else:
            if not os.path.isfile(fn):
                raise Exception("No such file " + fn)
    
        self.conn = sqlite3.connect(fn)
        self.c  = self.conn.cursor()
        if fresh:
            self.c.executescript(sql)

    def testdata(self):
        self.c.executescript(test_data)

    def raw_sql(self, data):
        self.c.executescript(data)

    def query(self, query):
        self.c.execute(query)
        return self.c.fetchall()

