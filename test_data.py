test_data="""
insert into graphs values (1, 1, 0);
insert into nodes values (1, 1, "A");
insert into nodes values (1, 2, "B");
insert into nodes values (1, 3, "C");
insert into nodes values (1, -3, "D");
insert into edges values (1, 2, NULL);
insert into edges values (1, 3, NULL);
insert into edges values (3, -3, NULL);

insert into graphs values (2, 1, 0);
insert into nodes values (2, 4, "A");
insert into nodes values (2, 5, "B");
insert into nodes values (2, 6, "C");
insert into nodes values (2, -6, "E");

insert into edges values (4, 5, NULL);
insert into edges values (4, 6, NULL);
insert into edges values (4, -6, NULL);

insert into nodes values (2, 7, "D");
insert into edges values  (6, 7, NULL);


insert into graphs values(3, 1, 1);
insert into nodes values (3, 8, "A");
insert into nodes values (3, 9, "B");
insert into nodes values (3, 10, "X");

insert into edges values (8, 9, NULL);
insert into edges values (8, 10, NULL);


insert into graphs values (4,1, 0);
insert into nodes values (4, 11, "A");
insert into nodes values (4, 12, "X");
insert into nodes values (4, 13, "B");
insert into nodes values (4, 14, "D");

insert into edges values (11, 12, NULL);
insert into edges values (11, 13, NULL);
insert into edges values (12, 14, NULL);
"""
