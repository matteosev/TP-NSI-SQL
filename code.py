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
    Ajoute un utilisateur dans la table "Utilisateur" de la base de données

    Paramètres:
        dbConnection (sqlite3.Connection object):
            la connexion vers la base de données dans laquelle ajouter un utilisateur
        user (list):
            une liste contenant
            - l'id (int)
            - le nom (str)
            - le prénom (str)
            de l'utilisateur à ajouter dans la base de données
            
    Valeur de retour:
        None
    """
    # permet de récupérer des objets "Row" avec la méthode fetchone, ce sont des
    # sortes de dictionnaires qui contiennent les noms des colonnes
    dbConnection.row_factory = sqlite3.Row
    cursor = dbConnection.cursor()
    cursor.execute("SELECT * FROM Acces")
    print(cursor.fetchone().keys())
    dbConnection.row_factory = None
    dbConnection.commit()
    cursor.close()

def DeleteUser(dbConnection, ID):
    """
    Supprime un utilisateur dans la table "Utilisateur" de la base de données

    Paramètres:
        dbConnection (sqlite3.Connection object):
            la connexion vers la base de données dans laquelle supprimer un utilisateur
        ID (int):
            l'identifiant de l'utilisateur à supprimer
    """
    pass

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
    #ExecuteScriptOnDB(dbFilename, "peupler_tables.sql")

    AddTableRow(dbConnection, "Acces", None)
    print(GetTableContent(dbConnection, "Utilisateur"))
    dbConnection.close()

    
