import sqlite3
import tkinter as tk
from code import *

# on redéfinit la fonction pour bind chaque cellule du tableau
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
    colNames = GetColumnNames(dbConnection, tableName)
    content = GetContent(dbConnection, tableName)
    
    for widget in frame.winfo_children():
        widget.destroy()

    for col in range(len(colNames)):
        tk.Label(frame, text = colNames[col]).grid(row = 0, column = col)

    entryVariables = []
    for row in range(len(content)):
        entryVariables.append([])   # nouvelle ligne
        for col in range(len(content[row])):
            entryVariables[row].append(tk.StringVar())
            entryVariables[row][col].set(content[row][col])
            entry = tk.Entry(frame, textvariable = entryVariables[row][col])
            entry.grid(row = row + 1, column = col)

# TODO: faire un bouton "enregistrer" qui ne marche que quand un élément a été changé

if __name__ == "__main__":
    dbConnection = sqlite3.connect("db.db")
    
    root = tk.Tk()
    root.title("Modification d'une base de données")
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)

    tableau = tk.Frame(root, relief="ridge", bd=1)
    interface = tk.Frame(root)
    tableau.grid(row=0, column=0)
    interface.grid(row=0, column=1)
    
    tables = GetTableNames(dbConnection)
    choix = tk.StringVar()
    choix.trace("w", lambda x, y, z: PrintTable(tableau, dbConnection, choix.get()))
    choix.set(tables[0])
    menu = tk.OptionMenu(interface, choix, *tables)
    menu.grid(row=0, column=0)
    commitBtn = tk.Button(interface, text="Commit")
    commitBtn.grid()

    root.mainloop()
    dbConnection.close()
