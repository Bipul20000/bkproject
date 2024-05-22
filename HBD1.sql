show databases;
create database project;

use project;
create table items (
    IName varchar(50),
    ICode char(4) primary key,
    price int,
    stock int
);

desc items;

insert into items values
("Ballpoint Pen", "BP01", 15, 50),
("Pencil", "PN02", 5, 100),
("Notebook", "NB03", 30, 20),
("Eraser", "ER04", 8, 40),
("Ruler", "RL05", 10, 30),
("Highlighter", "HL06", 20, 25),
("Stapler", "SP07", 50, 15),
("Sticky Notes", "SN08", 12, 35),
("Calculator", "CL09", 150, 10),
("Binder Clips", "BC10", 7, 60);

select * from items