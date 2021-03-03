import tkinter as tk
import tkinter.font as tkFont
import tkinter.messagebox as tkmsg
from tkinter.filedialog import askopenfilename
import sqlite3
from code import *


class app(tk.Tk):

    def __init__(self):
        self.dbConn = sqlite3.connect("db.db")
        tk.Tk.__init__(self)
        self.title("Logiciel de fou des Bg Matt, Cyp et Matth")
        self.createMenuBar()
        self.mainFrame = tk.Frame(self, relief="ridge", bd=2)
        self.mainFrame.grid()
        self.geometry("400x200")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.mainloop()


    def createMenuBar(self):
        menuBar = tk.Menu(self)

        fileMenu = tk.Menu(menuBar, tearoff=0)
        menuBar.add_cascade(label="Base de données", menu=fileMenu)
        fileMenu.add_command(label="Importer", command=self.openDB)
        fileMenu.add_command(label="Enregistrer", command=self.saveDB)

        tableNames = ("Utilisateur", "Responsable", "Acces", "Serrure", "Salle", "Batiment")
        
        addMenu = tk.Menu(menuBar, tearoff=0)
        for tableName in tableNames:
            addMenu.add_command(label=tableName, command=None)
        
        deleteMenu = tk.Menu(menuBar, tearoff=0)
        for tableName in tableNames:
            deleteMenu.add_command(label=tableName, command=None)
        
        viewMenu = tk.Menu(menuBar, tearoff=0)
        for tableName in tableNames:
            viewMenu.add_command(label=tableName, command=lambda n=tableName: self.showTable(n))
        
        menuBar.add_cascade(label="Ajouter", menu=addMenu)
        menuBar.add_cascade(label="Supprimer", menu=deleteMenu)
        menuBar.add_cascade(label="Consulter", menu=viewMenu)
        
        self.config(menu=menuBar)
        
        
    def openDB(self):
        fileName = askopenfilename(title="Importer une base de données", filetypes=[("Bases de données", ".db")])
        self.dbConn = sqlite3.connect(fileName)
        self.title(fileName)
        #tkmsg.showinfo(title="Importer une base de données", message="Base de données importée")


    def saveDB(self):
        askopenfilename(title="Enregistrer dans une base de données")
    
    def delFunction(self, tableName, nbLigne):
        content = GetContent(self.dbConn, tableName)
        deleteRowByValues(self.dbConn, tableName, content[nbLigne])
        
    def click(self, tableName, ligne, column):
        #print(content[0][0])
        Modification = tk.Tk()
        Modification.geometry('400x50')
        
        colNames = GetColumnNames(self.dbConn, tableName)
        content = GetContent(self.dbConn, tableName)
        
        entryList = [tk.Entry(Modification) for i in range(len(content[0]))]
        for col, entry in enumerate(entryList):
            entry.insert(-1, content[ligne][col])
            entry.grid(row=0, column=col)
        #self.wait_window()
        
        print(tableName)
        delButton = tk.Button(Modification, text = 'Supprimer', command = lambda: [delFunction(tableName), Modification.destroy()])
        delButton.grid(row=1)

    def showTable(self, tableName):
     
        labelList = []
        
        if self.dbConn == None:
            return
        
        for widget in self.mainFrame.winfo_children():
            widget.destroy()

        colNames = GetColumnNames(self.dbConn, tableName)
        content = GetContent(self.dbConn, tableName)

        self.mainFrame.rowconfigure(tuple(range(len(content) + 1)), weight=1)
        self.mainFrame.columnconfigure(tuple(range(len(colNames))), weight=1)

        labelFont = tkFont.Font(size=14)

        for col in range(len(colNames)):
            label = tk.Label(self.mainFrame, text = colNames[col], font=labelFont, padx=10, pady=10, relief="raised", bd=1)
            label.grid(row = 0, column = col, sticky="EW")
        
        for row in range(len(content)):
            for col in range(len(content[row])):
                label = tk.Label(self.mainFrame, text = content[row][col], padx=10, pady=10, font=labelFont)
                label.bind('<Button-1>', lambda a, row=row, col=col:self.click(tableName, row, col))
                label.grid(row = row + 1, column = col, sticky="EW")
        
def createCondition(colNames, values):
    sql = []
    values = list(values)
    for i in range(len(colNames)):
        if i > 0:
            sql.append(" AND ")
        if type(values[i]) == str:
            values[i] = "\"" + values[i] + "\""
        elif type(values[i]) == int:
            values[i] = str(values[i])
        sql.append(str(colNames[i]) + " = " + values[i])
    return "".join(sql)

def deleteRowByValues(dbConnection, tableName, values):
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
    dbConnection.execute(sql)
    
if __name__ == "__main__":
    
    app()

