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
                dbStrContent = list(map(str, dbContent[i]))
                selfStrContent = list(map(tk.StringVar.get, self.content[i]))
                
                dbHash = "".join(dbStrContent)
                selfHash = "".join(selfStrContent)

                if dbHash != selfHash:
                    print(dbStrContent, selfStrContent)
                    colNames = GetColumnNames(dbConnection, tableName)
                    condition = createCondition(colNames, dbStrContent)
                    Update(dbConnection, tableName, selfStrContent, condition)
                #print(DeleteRowByValues(dbConnection, tableName, list(map(tk.StringVar.get, self.content[i]))))

def createCondition(colNames, values):
    sql = []
    for i in range(len(colNames)):
        if i > 0:
            sql.append(" AND ")
        sql.append(colNames[i] + " = " + values[i])
    return "".join(sql)

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
    condition = createCondition(colNames, values)
    sql = "".join(["DELETE FROM " + tableName + " WHERE " + condition])
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
 
def changeTable(dbConnection, tableName, tkTable):
     global addParametersFrame

     tkTable.print(dbConnection, choix.get())
     
     for widget in addParametersFrame.winfo_children():
            widget.destroy()
            
     colNames = GetColumnNames(dbConnection, tableName)

     for i in range(len(colNames)):
         tk.Label(addParametersFrame, text=colNames[i]).grid(row=0, column=2*i)
         tk.Entry(addParametersFrame).grid(row=0, column=2*i+1)
         
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
    choix.set("")
    
    menuFrame = tk.Frame(interface)
    menuFrame.grid(row=0)
    menu = tk.OptionMenu(menuFrame, choix, *tables)
    menu.grid()
     
    addFrame = tk.Frame(interface)
    addFrame.grid(row=1, column=0)
    searchBtn = tk.Button(addFrame, text="Chercher")
    searchBtn.grid(row=0, column=0)
    addBtn = tk.Button(addFrame, text="Ajouter")
    addBtn.grid(row=0, column=1)
    delBtn = tk.Button(addFrame, text="Supprimer")
    delBtn.grid(row=0, column=2)
    addParametersFrame = tk.Frame(addFrame)
    addParametersFrame.grid(row=1, column=0)
    
    commitBtn = tk.Button(interface, text="Enregistrer", command=lambda:tableau.saveToDB(dbConnection, choix.get()))
    commitBtn.grid(row=2, column=0)
    
    choix.trace("w", lambda x, y, z: changeTable(dbConnection, choix.get(), tableau))
    choix.set(tables[0])

    root.mainloop()
    dbConnection.close()
