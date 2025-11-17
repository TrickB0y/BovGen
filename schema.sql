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
    semenMorfologiaEspermatica_id INTEGER UNIQUE
);