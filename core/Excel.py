import json
import win32com.client as win32  # installé par pip install pywin32
import os.path
from ReleveBanque.utils.ExcelWindowManager import ExcelWindowManager

class TablibError(Exception):
    pass


class Excel:
    """Classe pour gérer les opérations bancaires dans un fichier Excel."""
    EXIST, OPEN, NEW = range(3) 
     
    def __init__(self, acct:str, rep:str, worksheetname:str, modelpath:str):
        """Initialise l'objet COM Excel et affiche le classeur pour un compte donné.
        Args:
            acct (str): Le nom du compte bancaire.
            rep (str): Le répertoire où se trouve le fichier Excel.
            worksheetname (str): Le nom de la feuille de calcul à utiliser.
            modelpath (str): Le chemin vers le modèle Excel à utiliser pour créer un nouveau classeur."""
        
        self.WB = None      # Le classeur Excel
        self.hwnd = None    # Le handle de la fenêtre Excel
        self.WS = None      # La feuille de calcul Excel
        self.Appli = None   # L'application Excel

        wbname = acct + '.xlsx'             # Nom du classeur Excel pour le compte
        self.nomfic = rep + wbname          # Chemin complet du fichier Excel pour le compte
 
        self.mgr = ExcelWindowManager()     # Active ou crée une instance d'Excel
        self.Appli = self.mgr.appli           # On récupère l'instance Excel 
                
        self.Appli.Visible = True

        # On récupère la liste des classeurs ouverts 
        # et on vérifie si le classeur pour le compte existe déjà
        wbks = self.Appli.Workbooks
        openwbs= [w.Name for w in wbks]
        if wbname in openwbs:
                                                    # Récupère le classeur déjà ouvert
            self.WB = wbks[openwbs.index(wbname)]
            self.status = Excel.EXIST
        else:
            if os.path.exists(self.nomfic):
                self.WB = self.Appli.Workbooks.Open(self.nomfic)    #Ouvre le classeur existant
                self.status = Excel.OPEN
            else:
                self.WB = self.Appli.Workbooks.Add(modelpath)  # Crée un nouveau classeur à partir du modèle
                self.status = Excel.NEW
                # On crée un fichier tablib vide pour le compte
                with open(rep + acct + '.tablib', mode='w') as lib: 
                    lib.write('[]')

        # On active le classeur et on récupère le handle de la fenêtre Excel
        self.WB.Activate()
        # self.hwnd = find_hwnd_by_workbook_name(wbname)  

        # On récupère le hwnd à partir de la collection Windows du classeur
        # (on considère qu'il n'y a qu'une fenêtre)
        self.hwnd = self.mgr.hwnd = self.WB.Windows[0].Hwnd

        # On récupère la feuille de calcul "Banque" du classeur
        self.WS = self.WB.Worksheets(worksheetname)

        # Si le tableau est filtré, on affiche toutes les données 
        # pour éviter les problèmes d'ajout de ligne
        if (self.WS.AutoFilterMode and self.WS.FilterMode) or self.WS.FilterMode : 
            self.WS.ShowAllData()
        
        # On récupère la liste des lignes de la feuille de calcul Excel
        self.listRows = self.getlistRows()  # Traité par HTML_LBP

        # On charge le fichier tablib pour le compte
        with open(rep + acct + '.tablib', mode='r') as file:
            try:
                self.tablib = json.loads(file.read())
            except:
                raise TablibError('Erreur dans tablib')
        # Finalement, on retourne l'objet Excel initialisé
    
    #---------------------------------------------------------
    # Méthodes pour gérer les opérations dans le fichier Excel
    #---------------------------------------------------------

    def getLastRow(self) -> int:
        """Retourne le numéro de la dernière ligne utilisée dans la feuille de calcul Excel."""
        return self.listRows.Count

    def setVisibleRow(self, delta_row:int) -> None :
        """Se positionne sur la ligne delta_row° par rapport à la dernière ligne utilisée 
        pour assurer la visibilité de la ligne dans la fenêtre Excel.
        Args:
            delta_row (int): Le décalage (positif ou négatif)par rapport à la dernière ligne utilisée."""
        row = max(self.getLastRow()+delta_row, 1)
        self.Appli.Goto(self.WS.Cells(row, 1)) 

    def getStatus(self) -> int:
        """Retourne le statut du classeur Excel selon que le fichier était déjà ouvert, ouvert, ou nouveau."""
        return self.status

    def getStatusString(self) -> str:
        """Retourne une chaîne de caractères représentant le statut du classeur Excel."""
        return ["DEJA OUVERT", "OUVERTURE", "NOUVEAU"][self.status] 
    
    def saveWB(self) -> None:
        """Enregistre le classeur Excel selon son statut."""                        
        if self.status == Excel.NEW:
            self.WB.SaveAs(self.nomfic)
        else:
            self.WB.Save()
        
    def getRow(self, rownum:int) -> win32.CDispatch:  # Range Object
        """Retourne la ligne de la feuille de calcul Excel correspondant au numéro de ligne."""
        return self.listRows(rownum).Range

    def addRow(self) -> win32.CDispatch:    # Range object
        """Ajoute une ligne à la feuille de calcul Excel et retourne la plage de la nouvelle ligne."""
        ret = self.listRows.Add()
        return ret.Range

    def getXLOpe(self, row) -> XLOpe:
        """Retourne un objet XLOpe représentant l'opération bancaire dans la ligne Excel spécifiée."""                                                                  
        return self.XLOpe(self.getRow(row))
