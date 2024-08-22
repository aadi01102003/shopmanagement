create database shopmanagement;
use shopmanagement;
create table sellings(Sno int PRIMARY KEY,price int,quantity int);
create table employees(ID char(10) PRIMARY KEY,Age int,Salary int,No_of_Holiday_this_Month int,Phone_Number int);
create table user(username varchar(100),password varchar(200),Post varchar(200));