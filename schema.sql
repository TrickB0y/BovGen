DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Racas;
DROP TABLE IF EXISTS Localidades;
DROP TABLE IF EXISTS Animais;
DROP TABLE IF EXISTS TiposColeta;
DROP TABLE IF EXISTS Coletas;
DROP TABLE IF EXISTS ColetasEletroEjaculador;
DROP TABLE IF EXISTS ColetasVaginaArtificial;
DROP TABLE IF EXISTS ColetasEstimulacaoManual;

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
    coleta_id INTEGER NOT NULL,
    modo TEXT,
    intensidade TEXT,
    quantidadeEstimulos INTEGER,
    FOREIGN KEY (coleta_id) REFERENCES Coleta(id)
);

CREATE TABLE ColetasVaginaArtificial (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    coleta_id INTEGER NOT NULL,
    vacaORmanequim TEXT,
    vaca TEXT,
    FOREIGN KEY (coleta_id) REFERENCES Coleta(id)
);

CREATE TABLE ColetasEstimulacaoManual (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    coleta_id INTEGER NOT NULL,
    tempoMinutos INTEGER,
    FOREIGN KEY (coleta_id) REFERENCES Coleta(id)
);