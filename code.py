import sqlite3
from os import path

def ExecuteScriptOnDB(dbConnection, sqlFilename):
    """
    Modifie une base de données en exécutant le code contenu dans un fichier SQL

    Paramètres:
        dbConnection (sqlite3.Connection object):
            la connexion vers la base de données sur laquelle exécuter le script
        sqlFilename (str):
            le nom du fichier contenant le code SQL à exécuter

    Valeur de retour:
        None
    """
    sql = open(sqlFilename, "r").read()
    dbConnection.executescript(sql)
    dbConnection.commit()

def AddTableRow(dbConnection, tableName, row):
    """
    Ajoute une ligne dans une table.

    Paramètres:
        dbConnection (sqlite3.Connection object):
            la connexion vers la base de données à modifier
        tableName (str):
            le nom de la table dans laquelle ajouter une ligne
        row (list):
            les données de la ligne à ajouter
            
    Valeur de retour:
        None
    """
    for i in range(len(row)):
        if type(row[i]) == str:
            row[i] = "".join(["\"", row[i], "\""])
    rowString = "".join(["(", ",".join(map(str, row)), ")"])

    # permet de récupérer des objets "Row" avec la méthode fetchone, ce sont des
    # sortes de dictionnaires qui contiennent les noms des colonnes
    dbConnection.row_factory = sqlite3.Row
    cursor = dbConnection.cursor()
    cursor.execute("SELECT * FROM " + tableName)
    columnNames = "".join(["(", ",".join(cursor.fetchone().keys()), ")"])
    print("INSERT INTO " + tableName + columnNames + " VALUES " + rowString)
    cursor.execute("INSERT INTO " + tableName + columnNames + " VALUES " + rowString)

    dbConnection.row_factory = None
    dbConnection.commit()
    cursor.close()

def DeleteTableRow(dbConnection, tableName, idName, idValue):
    """
    Supprime une ligne dans une table

    Paramètres:
        dbConnection (sqlite3.Connection object):
            la connexion vers la base de données à modifier
        tableName (str):
            le nom de la table dans laquelle modifier une ligne
        idName (str):
            le nom de la colonne contenant la clé primaire
        idValue (str):
            la valeur de la clé primaire de la ligne à supprimer
    """
    pass
    #dbConnection.execute("DELETE FROM " + tableName + " WHERE 

def GetTableContent(dbConnection, tableName):
    """
    Retourne le contenu d'une table

    Paramètres:
        dbConnection (sqlite3.Connection object):
            la connexion vers la base de données dans laquelle chercher la table
        tableName (str):
            le nom de la table dont le contenu doit être retourné

    Valeur de retour (list):
        Une liste contenant les lignes de la table sous formes de tuples
    """
    content = []
    for row in dbConnection.execute("SELECT * FROM " + tableName):
        content.append(row)
    return content

if __name__ == "__main__":

    dbConnection = sqlite3.connect("db.db")
    ExecuteScriptOnDB(dbConnection, "creer_tables.sql")

    # décommenter pour peupler les tables
    #ExecuteScriptOnDB(dbConnection, "peupler_tables.sql")

    #AddTableRow(dbConnection, "Serrure", ["192.168.0.209"])
    #AddTableRow(dbConnection, "Utilisateur", [8, "reydet", "baptiste"])
    print(GetTableContent(dbConnection, "Utilisateur"))
    dbConnection.close()

    
