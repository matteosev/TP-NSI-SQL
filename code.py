import sqlite3
import tkinter as tk


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


def GetTableNames(dbConnection):
    """
    Retourne les noms des tables d'une base de données

    Paramètres:
        dbConnection (sqlite3.Connection):
            la connexion vers la base de données contenant la table à afficher

    Valeur de retour (list):
        Une liste contenant les noms des tables
    """
    cursor = dbConnection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type ='table' AND name NOT LIKE 'sqlite_%';")
    names = cursor.fetchall()
    for i in range(len(names)):
        names[i] = names[i][0]
    cursor.close()
    return names

    
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


def AddRow(dbConnection, tableName, colNames, row):
    """
    Ajoute une ligne dans une table.

    Paramètres:
        dbConnection (sqlite3.Connection):
            la connexion vers la base de données à modifier
        tableName (str):
            le nom de la table dans laquelle ajouter une ligne
        colNames (list):
            une liste contenant les noms des colonnes (str)
        row (list):
            les données de la ligne à ajouter
            
    Valeur de retour:
        None
    """
    # place des guillemets autour des données qui sont des chaînes de caractères
    for i in range(len(row)):
        if type(row[i]) == str:
            row[i] = "".join(["\"", row[i], "\""])

    # on crée une chaîne de la forme "(colonne1, colonne2, ...)
    colNames = "".join(["(", ",".join(colNames), ")"])

    # crée une chaîne de la forme "(donnée1, donnée2, ...)"
    row = "".join(["(", ",".join(map(str, row)), ")"])
    
    sql = "INSERT INTO " + tableName + columnNames + " VALUES " + row
    dbConnection.execute(sql)
    dbConnection.commit()
    print(sql)  # debuggage


def DeleteRowById(dbConnection, tableName, idName, idValue):
    """
    Supprime une ligne dans une table en fonction de son id

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


def Update(dbConnection, tableName, values, condition):
    """
    Modifie un enregistrement dans une base de données

    Paramètres:
        dbConnection (sqlite3.Connection):
            la connexion vers la base de données à modifier
        tableName (str):
            le nom de la table à modifier
        values (tuple):
            les valeurs de l'enregistrement dans l'ordre des colonnes
        condition (str):
            une condition SQL à appliquer pour sélectionner l'enregistrement à modifier

    Valeur de retour:
        None
    """
    setParameters = []
    colNames = GetColumnNames(dbConnection, tableName)
    for i in range(len(colNames)):
        if type(values[i]) == str:
            values[i] = "".join(["\"", values[i], "\""])
        setParameters.append(colNames[i] + " = " + values[i])
    setParameters = ",".join(setParameters)
    sql = "UPDATE " + tableName + " SET " + setParameters + " WHERE " + condition
    print(sql)
    dbConnection.execute(sql)
    dbConnection.commit()
    

def PrintTable(frame, colNames, content):
    """
    Affiche une table dans une frame tkinter.

    Paramètres:
        frame (tkinter.Frame):
            la frame dans laquelle afficher la table
        colNames (list):
            une liste contenant les noms des colonnes
        content (list):
            une liste (lignes) de listes (colonnes) contenant les données de la table

    Valeur de retour:
        None
    """
    for widget in frame.winfo_children():
        widget.destroy()

    for col in range(len(colNames)):
        tk.Label(frame, text = colNames[col]).grid(row = 0, column = col)

    for row in range(len(content)):
        for col in range(len(content[row])):
            tk.Label(frame, text = content[row][col]).grid(row = row + 1, column = col)


if __name__ == "__main__":
    
    dbConnection = sqlite3.connect("db.db")
    ExecuteScriptOnDB(dbConnection, "creer_tables.sql")

    # décommenter pour peupler les tables
    #ExecuteScriptOnDB(dbConnection, "peupler_tables.sql")

    # prototype d'interface
    root = tk.Tk()
    root.title("Gestionnaire de base de données")
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=2)
    root.columnconfigure(1, weight=2)
    root["bg"] = "bisque"

    tableau = tk.Frame(root)
    interface = tk.Frame(root)
    tableau.grid(row=0, column=0)
    interface.grid(row=0, column=1)
    
    menuButton = tk.Menubutton(interface, text="Choisissez une table")
    menuButton.menu = tk.Menu(menuButton)
    menuButton["menu"] = menuButton.menu
    
    tables = ("Acces", "Batiment", "Responsable", "Salle", "Serrure", "Situer", "Utilisateur")
    choix = tk.StringVar()
    choix.trace("w", lambda x, y, z: PrintTable(tableau, GetColumnNames(dbConnection, choix.get()), GetContent(dbConnection, choix.get())))
    choix.set("Utilisateur")
    menu = tk.OptionMenu(interface, choix, *tables)
    #addBtn = tk.Button(interface, text="Ajouter une ligne", command=AddRow(dbConnection, choix, "", ""))
    menu.grid(row=0, column=0)

    root.mainloop()
    dbConnection.close()

    
