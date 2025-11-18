DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Racas;
DROP TABLE IF EXISTS Localidades;
DROP TABLE IF EXISTS Animais;
DROP TABLE IF EXISTS TiposColeta;
DROP TABLE IF EXISTS Coletas;
DROP TABLE IF EXISTS ColetasEletroEjaculador;
DROP TABLE IF EXISTS ColetasVaginaArtificial;
DROP TABLE IF EXISTS ColetasEstimulacaoManual;
DROP TABLE IF EXISTS SemensCaracteristicas;
DROP TABLE IF EXISTS SemensParametrosDoConjunto;
DROP TABLE IF EXISTS SemensMorfologiaEspermatica;
DROP TABLE IF EXISTS Semens;
DROP TABLE IF EXISTS Botijoes;
DROP TABLE IF EXISTS Canecos;
DROP TABLE IF EXISTS Racks;


CREATE TABLE Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    login TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE Racas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE Localidades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_fazenda TEXT UNIQUE NOT NULL,
    estado TEXT NOT NULL,
    cidade TEXT NOT NULL
);

CREATE TABLE Animais (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rgd TEXT UNIQUE NOT NULL,
    raca_id INTEGER,
    nome TEXT NOT NULL,
    sexo TEXT NOT NULL,
    categoria TEXT,
    nascimento TEXT,
    localidade_id INTEGER,
    pai_id INTEGER,
    mae_id INTEGER,
    propietario TEXT,
    FOREIGN KEY (pai_id) REFERENCES Animais(id),
    FOREIGN KEY (mae_id) REFERENCES Animais(id)
);

CREATE TABLE TiposColeta (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL
);

INSERT INTO TiposColeta(nome) VALUES
('Eletro Ejaculador'),
('Vagina Artificial'),
('Estimulação Manual');

CREATE TABLE Coletas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    animal_id INTEGER NOT NULL,
    dataColeta DATE NOT NULL,
    tipoColeta_id INTEGER NOT NULL,
    dadosColeta_id INTEGER,
    sucesso TEXT NOT NULL,
    exposicao TEXT NOT NULL,
    anotacao TEXT,
    quantidade INTEGER,
    FOREIGN KEY (animal_id) REFERENCES Animais(id),
    FOREIGN KEY (tipoColeta_id) REFERENCES TipoColeta(id)
);

CREATE TABLE ColetasEletroEjaculador (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    coleta_id INTEGER NOT NULL UNIQUE,
    modo TEXT,
    intensidade TEXT,
    quantidadeEstimulos INTEGER,
    FOREIGN KEY (coleta_id) REFERENCES Coleta(id)
);

CREATE TABLE ColetasVaginaArtificial (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    coleta_id INTEGER NOT NULL UNIQUE,
    vacaORmanequim TEXT,
    vaca TEXT,
    FOREIGN KEY (coleta_id) REFERENCES Coleta(id)
);

CREATE TABLE ColetasEstimulacaoManual (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    coleta_id INTEGER NOT NULL UNIQUE,
    tempoMinutos INTEGER,
    FOREIGN KEY (coleta_id) REFERENCES Coleta(id)
);

CREATE TABLE SemensCaracteristicas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    semen_id INTEGER NOT NULL UNIQUE,
    contaminacao TEXT,
    quantidade INTEGER,
    consistencia TEXT,
    peso INTEGER,
    cor TEXT,
    anotacao TEXT,
    FOREIGN KEY (semen_id) REFERENCES Semens(id)
);

CREATE TABLE SemensParametrosDoConjunto (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    semen_id INTEGER NOT NULL UNIQUE,
    motilidade INTEGER,
    motilidadeAprovacao TEXT,
    vigor INTEGER,
    vigorAprovacao TEXT,
    concentracao INTEGER,
    concentracaoAprovacao TEXT,
    FOREIGN KEY (semen_id) REFERENCES Semens(id)
);

CREATE TABLE SemensMorfologiaEspermatica (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    semen_id INTEGER NOT NULL UNIQUE,
    normalContagem INTEGER,
    acromossomaContagem INTEGER,
    gotaProximalContagem INTEGER,
    cabecaPequenaContagem INTEGER,
    caldaEnroladaCabecaContagem INTEGER,
    cabecaIsoladaPatologicaContagem INTEGER,
    cabecaEstreitaBaseContagem INTEGER,
    cabecaPiriformeContagem INTEGER,
    cabecaPequenaNormalContagem INTEGER,
    cabecaColoracaoAnormalContagem INTEGER,
    cabecaContornoAnormalContagem INTEGER,
    pouchFormationContagem INTEGER,
    cabecaUlceradaContagem INTEGER,
    caldaDobradaContagem INTEGER,
    formasTeratogenicaContagem INTEGER,
    pecaIntermediariaContagem INTEGER,
    caldaFortementeDobradaContagem INTEGER,
    caldaDobradaGotaDistalContagem INTEGER,
    cabecaDelgadaContagem INTEGER,
    cabecaGiganteContagem INTEGER,
    cabecaIsoladaNormalContagem INTEGER,
    abaxialContagem INTEGER,
    obliquoContagem INTEGER,
    gotaDistalContagem INTEGER,
    totalAprovado TEXT,
    FOREIGN KEY (semen_id) REFERENCES Semens(id)
);

CREATE TABLE Semens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    coleta_id INTEGER NOT NULL UNIQUE,
    semenCaracteristicas_id INTEGER UNIQUE,
    semenParametrosDoConjunto_id INTEGER UNIQUE,
    semenMorfologiaEspermatica_id INTEGER UNIQUE,
    FOREIGN KEY (semenCaracteristicas_id) REFERENCES SemensCaracteristicas(id),
    FOREIGN KEY (semenParametrosDoConjunto_id) REFERENCES SemensParametrosDoConjunto(id),
    FOREIGN KEY (semenMorfologiaEspermatica_id) REFERENCES SemensMorfologiaEspermatica(id)
);

CREATE TABLE Botijoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    caneco1_id INTEGER UNIQUE,
    caneco2_id INTEGER UNIQUE,
    caneco3_id INTEGER UNIQUE,
    caneco4_id INTEGER UNIQUE,
    caneco5_id INTEGER UNIQUE,
    caneco6_id INTEGER UNIQUE,
    FOREIGN KEY (caneco1_id) REFERENCES Canecos(id),
    FOREIGN KEY (caneco2_id) REFERENCES Canecos(id),
    FOREIGN KEY (caneco3_id) REFERENCES Canecos(id),
    FOREIGN KEY (caneco4_id) REFERENCES Canecos(id),
    FOREIGN KEY (caneco5_id) REFERENCES Canecos(id),
    FOREIGN KEY (caneco6_id) REFERENCES Canecos(id)
);

CREATE TABLE Canecos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    botijao_id INTEGER NOT NULL,
    cor TEXT NOT NULL,
    FOREIGN KEY (botijao_id) REFERENCES Botijoes(id)
);

CREATE TABLE Racks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    botijao_id INTEGER NOT NULL,
    caneco_id INTEGER NOT NULL,
    semen_id INTEGER NOT NULL,
    quantidade INTEGER,
    anotacao TEXT
);

INSERT INTO Botijoes(nome) 
VALUES 
('Congelamento'),
('Aulas e projeto de pesquisa'),
('Sêmem para inseminação e produção de embrião'),
('semem para comercialização');

INSERT INTO Canecos(botijao_id, cor)
VALUES
(1,'Amarelo'),
(1,'Azul'),
(1,'Branco'),
(1,'Vermelho'),
(1,'Verde'),
(1,'Preto');

UPDATE Botijoes SET caneco1_id = 1, caneco2_id = 2, caneco3_id = 3, caneco4_id = 4, caneco5_id = 5, caneco6_id = 6 WHERE id = 1;

INSERT INTO Canecos(botijao_id, cor)
VALUES
(2,'Amarelo'),
(2,'Azul'),
(2,'Branco'),
(2,'Vermelho'),
(2,'Verde'),
(2,'Preto');

UPDATE Botijoes SET caneco1_id = 7, caneco2_id = 8, caneco3_id = 9, caneco4_id = 10, caneco5_id = 11, caneco6_id = 12 WHERE id = 2;

INSERT INTO Canecos(botijao_id, cor)
VALUES
(3,'Amarelo'),
(3,'Azul'),
(3,'Branco'),
(3,'Vermelho'),
(3,'Verde'),
(3,'Preto');

UPDATE Botijoes SET caneco1_id = 13, caneco2_id = 14, caneco3_id = 15, caneco4_id = 16, caneco5_id = 17, caneco6_id = 18 WHERE id = 3;

INSERT INTO Canecos(botijao_id, cor)
VALUES
(4,'Amarelo'),
(4,'Azul'),
(4,'Branco'),
(4,'Vermelho'),
(4,'Verde'),
(4,'Preto');

UPDATE Botijoes SET caneco1_id = 19, caneco2_id = 20, caneco3_id = 21, caneco4_id = 22, caneco5_id = 23, caneco6_id = 24 WHERE id = 4;