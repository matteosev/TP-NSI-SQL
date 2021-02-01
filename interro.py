import sqlite3
import tkinter as tk
from code import *

class TkTable(tk.Frame):
    """
    Une table de base de données affichée dans une frame
    """
    
    def __init__(self, parent, dbConnection, tableName):
        """
        Paramètres:
            parent (tkinter.Frame):
                la frame contenant la table
            dbConnection (sqlite3.Connection):
                la connexion vers la base de données contenant la table à afficher
            tableName (str):
                le nom de la table à afficher
        """
        tk.Frame.__init__(self, parent)
        self.print(dbConnection, tableName)

    def print(self, dbConnection, tableName):

        for widget in self.winfo_children():
            widget.destroy()
        
        self.content = []
        colNames = GetColumnNames(dbConnection, tableName)
        content = GetContent(dbConnection, tableName)
        
        for col in range(len(colNames)):
            tk.Label(self, text = colNames[col]).grid(row = 0, column = col)
        
        for row in range(len(content)):
            self.content.append([])   # nouvelle ligne
            for col in range(len(content[row])):
                self.content[row].append(tk.StringVar())
                self.content[row][col].set(content[row][col])
                entry = tk.Entry(self, textvariable = self.content[row][col])
                entry.grid(row = row + 1, column = col)

                
    def saveToDB(self, dbConnection, tableName):
        """
        Enregistre le contenu de la TkTable dans une table

        Paramètres:
            dbConnection (sqlite3.Connection):
                la connexion vers la base de données contenant la table à afficher
            tableName (str):
                le nom de la table dans laquelle enregistrer les données

        Valeur de retour (str):
            None
        """
        colNames = GetColumnNames(dbConnection, tableName)
        dbContent = GetContent(dbConnection, tableName)
        dbLen = len(dbContent)
        selfLen = len(self.content)

        if selfLen < dbLen:
            for i in range(selfLen, dbLen):
                # supprimer les lignes superflues
                pass

        for i in range(selfLen):
            if i > dbLen:
                # ajouter une ligne à la base de données
                pass
            else:
                dbHash = "".join(list(map(str, dbContent[i])))
                selfHash = "".join(list(map(tk.StringVar.get, self.content[i])))

                if dbHash != selfHash:
                    pass
                print(DeleteRowByValues(dbConnection, tableName, list(map(tk.StringVar.get, self.content[i]))))


def DeleteRowByValues(dbConnection, tableName, values):
    """
    Supprime une ligne dans une table en fonction de ses valeurs

    Paramètres:
        dbConnection (sqlite3.Connection):
            la connexion vers la base de données à modifier
        tableName (str):
            le nom de la table dans laquelle modifier une ligne
        values (tuple):
            les valeurs de la ligne à supprimer

    Valeur de retour:
        None
    """
    colNames = GetColumnNames(dbConnection, tableName)
    sql = ["DELETE FROM " + tableName + " WHERE "]
    for i in range(len(colNames)):
        if i > 0:
            sql.append(" AND ")
        sql.append(colNames[i] + " = " + values[i])
    sql = "".join(sql)
    print(sql)


def UpdateTable(dbConnection, tableName, newContent):
    """
    Modifie une table dans une base de données.

    Paramètres:
        dbConnection (sqlite3.Connection):
            la connexion vers la base de données contenant la table à afficher
        tableName (str):
            le nom de la table à afficher
        newContent (list):
            une liste contenant des listes représentant les lignes de la table,
            ces listes contiennent les données au format str

    Valeur de retour:
        None
    """
    if GetContent(dbConnection, tableName) == newContent:
        print("=")
        return
    
# TODO: faire un bouton "enregistrer" qui ne marche que quand un élément a été changé

if __name__ == "__main__":
    dbConnection = sqlite3.connect("db.db")
    
    root = tk.Tk()
    root.title("Modification d'une base de données")
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)

    tableau = TkTable(root, dbConnection, "Utilisateur")
    tableau.grid(row=0, column=0)
    
    interface = tk.Frame(root)
    interface.grid(row=0, column=1)

    tables = GetTableNames(dbConnection)
    choix = tk.StringVar()
    choix.trace("w", lambda x, y, z: tableau.print(dbConnection, choix.get()))
    choix.set(tables[0])
    
    menu = tk.OptionMenu(interface, choix, *tables)
    menu.grid(row=0, column=0)
 
    commitBtn = tk.Button(interface, text="Commit", command=lambda: tableau.saveToDB(dbConnection, choix.get()))
    commitBtn.grid()

    root.mainloop()
    dbConnection.close()
