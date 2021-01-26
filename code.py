import sqlite3


def ExecuteScriptOnDB(dbConnection, sqlFilename):
    """
    Modifie une base de données en exécutant le code contenu dans un fichier SQL

    Paramètres:
        dbConnection (sqlite3.Connection):
            la connexion vers la base de données sur laquelle exécuter le script
        sqlFilename (str):
            le nom du fichier contenant le code SQL à exécuter

    Valeur de retour:
        None
    """
    sql = open(sqlFilename, "r").read()
    dbConnection.executescript(sql)
    dbConnection.commit()


def GetColumnNames(dbConnection, tableName):
    """
    Retourne les noms des colonnes d'une table

    Paramètres:
        dbConnection (sqlite3.Connection):
            la connexion vers la base de données
        tableName (str):
            le nom de la table dont les noms de colonnes doivent être retournés

    Valeur de retour (list):
        une liste de chaînes de caractères, les noms des colonnes
    """
    oldRow_factory = dbConnection.row_factory
    # permet de récupérer des objets "Row" avec la méthode fetchone, ce sont des
    # sortes de dictionnaires qui contiennent les noms des colonnes
    dbConnection.row_factory = sqlite3.Row
    cursor = dbConnection.cursor()
    cursor.execute("SELECT * FROM " + tableName)
    columns = cursor.fetchone().keys()
    dbConnection.row_factory = oldRow_factory
    cursor.close()
    return columns


def GetContent(dbConnection, tableName):
    """
    Retourne le contenu d'une table

    Paramètres:
        dbConnection (sqlite3.Connection):
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


def AddRow(dbConnection, tableName, row):
    """
    Ajoute une ligne dans une table.

    Paramètres:
        dbConnection (sqlite3.Connection):
            la connexion vers la base de données à modifier
        tableName (str):
            le nom de la table dans laquelle ajouter une ligne
        row (list):
            les données de la ligne à ajouter
            
    Valeur de retour:
        None
    """
    # place des guillemets autour des données qui sont des chaînes de caractères
    for i in range(len(row)):
        if type(row[i]) == str:
            row[i] = "".join(["\"", row[i], "\""])
    # crée une chaîne de caractère de la forme "(donnée1, donnée2, ...)"
    row = "".join(["(", ",".join(map(str, row)), ")"])

    columnNames = GetColumnNames(dbConnection, tableName)
    # on crée une chaîne de la forme "(colonne1, colonne2, ...)
    columnNames = "".join(["(", ",".join(columnNames), ")"])
    
    sql = "INSERT INTO " + tableName + columnNames + " VALUES " + row
    dbConnection.execute(sql)
    dbConnection.commit()
    print(sql)  # debuggage


def DeleteRow(dbConnection, tableName, idName, idValue):
    """
    Supprime une ligne dans une table

    Paramètres:
        dbConnection (sqlite3.Connection):
            la connexion vers la base de données à modifier
        tableName (str):
            le nom de la table dans laquelle modifier une ligne
        idName (str):
            le nom de la colonne contenant la clé primaire
        idValue (str):
            la valeur de la clé primaire de la ligne à supprimer

    Valeur de retour:
        None
    """
    idName = "".join(["\"", idName, "\""])
    idValue = "".join(["\"", str(idValue), "\""])
    sql = "DELETE FROM " + tableName + " WHERE " + idName + " = " + idValue
    dbConnection.execute(sql)
    dbConnection.commit()
    print(sql)  # debuggage


def Update(dbConnection, tableName, newRecord, condition):
    """
    Modifie un enregistrement dans une base de données

    Paramètres:
        dbConnection (sqlite3.Connection):
            la connexion vers la base de données à modifier
        tableName (str):
            le nom de la table à modifier
        values (dict):
            les noms des colonnes auxquelles correspondent les valeurs
            ex: Update(..., {"colonne1": value1, "colonne2": value2}, ...)
        condition (str):
            une condition SQL à appliquer pour sélectionner l'enregistrement à modifier

    Valeur de retour:
        None
    """
    setParameters = []
    recordKeys = list(map(str, newRecord.keys()))
    recordValues = list(map(str, newRecord.values()))
    for i in range(len(recordKeys)):
        if type(recordValues[i]) == str:
            recordValues[i] = "".join(["\"", recordValues[i], "\""])
        setParameters.append(recordKeys[i] + " = " + recordValues[i])
    setParameters = ",".join(setParameters)
    sql = "UPDATE " + tableName + " SET " + setParameters + " WHERE " + condition
    print(sql)
    dbConnection.execute(sql)
    dbConnection.commit()
    

def PrintTable(frame, dbConnection, tableName):
    """
    Affiche une table dans une frame tkinter.

    Paramètres:
        frame (tkinter.Frame):
            la frame dans laquelle afficher la table
        dbConnection (sqlite3.Connection):
            la connexion vers la base de données contenant la table à afficher
        tableName (str):
            le nom de la table à afficher

    Valeur de retour:
        None
    """
    content = GetContent(dbConnection, tableName)

    for widget in frame.winfo_children():
        widget.destroy()

    for row in range(len(content)):
        for column in range(len(content[row])):
            tk.Label(frame, text = content[row][column]).grid(row = row, column = column)



if __name__ == "__main__":
    import tkinter as tk

    root = tk.Tk()
    root.title("Gestionnaire de base de données")
    root["bg"] = "bisque"

    tableau = tk.Frame(root)
    tableau.pack()
    
    dbConnection = sqlite3.connect("db.db")
    ExecuteScriptOnDB(dbConnection, "creer_tables.sql")

    # décommenter pour peupler les tables
    #ExecuteScriptOnDB(dbConnection, "peupler_tables.sql")

    # prototype d'interface
    menuButton = tk.Menubutton(root, text="Choisissez une table")
    menuButton.menu = tk.Menu(menuButton)
    menuButton["menu"] = menuButton.menu
    userVar = tk.IntVar()
    adminVar = tk.IntVar()
    menuButton.menu.add_command(label="Utilisateur", command=lambda: PrintTable(tableau, dbConnection, "Utilisateur"))
    menuButton.menu.add_command(label="Responsable", command=lambda: PrintTable(tableau, dbConnection, "Responsable"))
    menuButton.pack()

    root.mainloop()
    dbConnection.close()

    
