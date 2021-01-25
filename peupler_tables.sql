INSERT INTO Salle
(id, numero, etage)
VALUES
(1, 17, 2),
(2, 12, 1),
(3, 4, 1);

INSERT INTO Responsable
(id, nom, prenom)
VALUES
(1, "Simpson", "Bart"),
(2, "Lovelace", "Ada"),
(3, "Dupot", "Francis");

INSERT INTO Utilisateur
(id, nom, prenom)
VALUES
(1, "Jovovich", "Mila"),
(2, "Skiwalker", "Louke"),
(3, "Pignouf", "Gerard");

INSERT INTO Serrure
(addresse_mac)
VALUES
("192.168.0.45"),
("192.168.0.28"),
("192.168.0.78"),
("192.168.0.126"),
("192.168.0.107");

INSERT INTO Batiment
(id)
VALUES
(1),
(2);

INSERT INTO Acces
(idSalle, idUtilisateur, jour, plage)
VALUES
(1, 2, 3, 5);

INSERT INTO Situer
(idBatiment, idSalle)
VALUES
(1, 3),
(2, 1),
(2, 2);

