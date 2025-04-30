create database projeto_game;
use projeto_game;

create table Usuario(
    id_usuario int primary key not null auto_increment,
    nome varchar(100) not null,
    email varchar(100) not null,
    senha varchar(20) not null
);

create table Jogador(
    id_jogador int primary key not null auto_increment,
    nome varchar(100) not null, 
    record time,  
    id_usuario int,  
    foreign key (id_usuario) references Usuario(id_usuario) 
);

ALTER TABLE Usuario
ADD COLUMN  id_jogador INT;

ALTER TABLE Usuario
ADD CONSTRAINT id_jogador
foreign key (id_jogador) references Jogador(id_jogador);

