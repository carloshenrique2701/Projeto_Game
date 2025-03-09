create database Jogo_Dados;

use Jogo_Dados;

create table Usuario(
	Id int primary key not null,
	nome varchar(100) not null,
    idade date not null,
    email varchar(100)not null,
    senha varchar(20) not null
);

create table Jogador(
	nome varchar(20) not null,
    record time 
);
