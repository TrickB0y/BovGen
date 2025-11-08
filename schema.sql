DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Racas;
DROP TABLE IF EXISTS Localidades;
DROP TABLE IF EXISTS Animais;

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