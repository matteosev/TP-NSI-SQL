import sqlite3
import tkinter as tk
from code import *

# on redéfinit la fonction pour bind chaque cellule du tableau
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
            label = tk.Label(frame, text = content[row][col])
            label.bind('<Button-1>', lambda click: AskModif(click))
            label.grid(row = row + 1, column = col)


def AskModif(click):
    global tableau
    print(click.x, click.y)
    print(tableau.grid_size())
    #print(tableau.grid_location(click.x, click.y))

if __name__ == "__main__":
    dbConnection = sqlite3.connect("db.db")
    
    root = tk.Tk()
    root.title("Modification d'une base de données")
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=2)
    root.columnconfigure(1, weight=2)

    tableau = tk.Frame(root, relief="ridge", bd=1)
    interface = tk.Frame(root)
    tableau.grid(row=0, column=0)
    interface.grid(row=0, column=1)
    
    tables = GetTableNames(dbConnection)
    choix = tk.StringVar()
    choix.trace("w", lambda x, y, z: PrintTable(tableau, GetColumnNames(dbConnection, choix.get()), GetContent(dbConnection, choix.get())))
    choix.set(tables[0])
    menu = tk.OptionMenu(interface, choix, *tables)
    menu.grid(row=0, column=0)
    commitBtn = tk.Button(interface, text="Commit")
    commitBtn.grid()

    root.mainloop()
    dbConnection.close()