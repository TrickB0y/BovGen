DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Racas;
DROP TABLE IF EXISTS Localidades;
DROP TABLE IF EXISTS Animais;
DROP TABLE IF EXISTS TipoColeta;
DROP TABLE IF EXISTS Coleta;

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

CREATE TABLE TipoColeta (
    id INTEGER NOT NULL,
    nome TEXT NOT NULL
);

INSERT INTO TipoColeta(nome) VALUES
('Eletro Ejaculador'),
('Vagina Artificial'),
('Estimulação Manual');

CREATE TABLE Coleta (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    animal_id INTEGER NOT NULL,
    dataColeta DATE NOT NULL,
    tipoColeta_id INTEGER NOT NULL,
    dadoColeta_id INTEGER,
    #sucesso é bool 'SIM' ou 'NÃO'
    sucesso TEXT NOT NULL,
    #exposicao é bool 'SIM' ou 'NÃO'
    exposicao TEXT NOT NULL,
    anotacao TEXT,
    quantidade INTEGER,
    FOREIGN KEY (animal_id) REFERENCES Animais(id),
    FOREIGN KEY (tipoColeta_id) REFERENCES TipoColeta(id)
);

CREATE TABLE EletroEjaculador (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    coleta_id INTEGER NOT NULL,
    modo TEXT,
    intensidade TEXT,
    #quantidade 0..30
    quantidadeEstimulos INTEGER,
    FOREIGN KEY (coleta_id) REFERENCES Coleta(id)
);

CREATE TABLE VaginaArtificial (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    coleta_id INTEGER NOT NULL,
    vacaORmanequin TEXT,
    vaca TEXT,
    FOREIGN KEY (coleta_id) REFERENCES Coleta(id)
);

CREATE TABLE EstimulacaoManual (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    coleta_id INTEGER NOT NULL,
    tempoMinutos INTEGER,
    FOREIGN KEY (coleta_id) REFERENCES Coleta(id)
);