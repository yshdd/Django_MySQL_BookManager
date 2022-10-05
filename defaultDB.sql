create database library;
use library;

-- 一つ目のテーブル
create table students(
    stuID int primary key,
    stuName char(100) not null,
);
#人の追加
insert into students VALUES (1, "山田");
insert into students VALUES (2, "高橋");
insert into students VALUES (3, "吉田");

-- 二つ目のテーブル
create table books(
    bookID int primary key,
    bookName char(100) NOT NULL,
		returned boolean default 0,
);
#本の追加
insert into books VALUES (1001, "XXX", 0);
insert into books VALUES (1002, "YYY", 0);
insert into books VALUES (1003, "ZZZ", 0);
insert into books VALUES (1004, "AAA", 0);
insert into books VALUES (1005, "BBB", 0);
insert into books VALUES (1006, "CCC", 1);
insert into books VALUES (1007, "DDD", 1);

-- 三つ目のテーブル
create table lend_date_stu(
    No int auto_increment primary key,
    date DATE,
    stuID int,
    foreign key(stuID) references students(stuID)
);

-- レコードの追加
insert into lend_date_stu VALUES (1, "20220401",1);
insert into lend_date_stu VALUES (2, "20220415",2);
insert into lend_date_stu VALUES (3, "20220430",3);

-- ４つ目のレコード
create table lend_books(
    No int,
    bookID int,
		id int auto_increment primary key,
    foreign key(No) references lend_date_stu(No),
    foreign key(bookID) references books(bookID)
);
#貸出された本の情報
insert into lend_books VALUES (1, 1001, 1);
insert into lend_books VALUES (1, 1002, 2);
insert into lend_books VALUES (1, 1003, 3);
insert into lend_books VALUES (2, 1004, 4);
insert into lend_books VALUES (3, 1005, 5);