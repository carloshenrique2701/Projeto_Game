create database Jogo_Dados;

/* Convertido para postgresql */;

-- SQLINES FOR EVALUATION USE ONLY (14 DAYS)
create table Usuario(
    id_usuario int primary key not null generated always as identity,
    nome varchar(100) not null,
    email varchar(100) not null,
    senha varchar(20) not null,
    id_jogador int,  
    foreign key (id_jogador) references Jogador(id_jogador)  
);

create table Jogador(
    id_jogador int primary key not null generated always as identity,
    nome varchar(100) not null, 
    record time(0),  
    id_usuario int,  
    foreign key (id_usuario) references Usuario(id_usuario) 
);
