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
    apelido varchar(100) not null, 
    record int,  
    show_in_rank boolean,
    id_usuario int not null,  
    foreign key (id_usuario) references Usuario(id_usuario) 
);


