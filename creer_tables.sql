CREATE TABLE IF NOT EXISTS Salle
(
	id INT PRIMARY KEY,
	numero INT,
	etage INT
);

CREATE TABLE IF NOT EXISTS Responsable
(
	id INT PRIMARY KEY,
	nom TEXT,
	prenom TEXT
);

CREATE TABLE IF NOT EXISTS Utilisateur
(
	id INT PRIMARY KEY,
	nom TEXT,
	prenom TEXT
);

CREATE TABLE IF NOT EXISTS Serrure
(
	addresse_mac TEXT PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS Batiment
(
	id INT PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS Acces
(
	idSalle INT,
	idUtilisateur INT,
	jour INT,
	plage INT,
	PRIMARY KEY (idSalle, idUtilisateur, jour, plage)
);

CREATE TABLE IF NOT EXISTS Situer
(
	idBatiment INT,
	idSalle INT,
	PRIMARY KEY (idBatiment, idSalle)
);
	