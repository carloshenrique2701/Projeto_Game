create database Jogo_Dados;

use Jogo_Dados;

create table Usuario(
    id_usuario int primary key not null auto_increment,
    nome varchar(100) not null,
    idade int not null,
    email varchar(100) not null,
    senha varchar(20) not null,
    id_jogador int,  
    foreign key (id_jogador) references Jogador(id_jogador)  
);

create table Jogador(
    id_jogador int primary key not null auto_increment,
    nome varchar(100) not null, 
    record time,  
    id_usuario int,  
    foreign key (id_usuario) references Usuario(id_usuario) 
);
