import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont
import queue
from ReleveBanque.utils import winmgt

# ============================================================
# GUI
# ============================================================
PINK = "#FFAED0"
GREY = "#B5B5B5"
import tkinter.font as tkfont

class MLFrame(tk.Frame):

    def __init__(self, parent, text, label_bg=GREY):
        super().__init__(parent, bd=3, relief="groove")
        fontBold = tkfont.nametofont('TkDefaultFont').copy()
        fontBold.configure(weight='bold')
        self.label = tk.Label(self, text=text, bg=label_bg, font=fontBold)
        self.label.pack(fill="x")

        self.content = tk.Frame(self)
        self.content.pack(fill="both", expand=True)

class gui:
    def __init__(self, root, gui_queue, metier_queue, geo):
        self.root=root
        self.geometry = geo
        self.metier_queue = metier_queue
        self.gui_queue = gui_queue
        self.oXL = None
        self.oHTML = None
        self.voir_Excel:bool = False
        #root.tk.call('tk', 'scaling', 1.5)
        scaling = float(root.tk.call('tk', 'scaling'))
        row_h = int(12 * scaling)   # 12 = hauteur "normale" de base
        root.title("Extraction des opérations bancaires")
        W = root.winfo_screenwidth()
        H = root.winfo_screenheight()
        self.ratio = W/1920
        root.geometry('1000x1000+500+500')
        fontBold = tkfont.nametofont('TkDefaultFont').copy()
        fontBold.configure(weight='bold')
        
        root.grid_rowconfigure(0, weight=0)  # Journal
        root.grid_rowconfigure(1, weight=0)  # Résultats
        root.grid_rowconfigure(2, weight=1)  # Tableau -> prend le reste
        root.grid_rowconfigure(3, weight=0)  # Boutons

        root.grid_columnconfigure(0, weight=1)
       
       # Journal
        bloc_log = MLFrame(root, text="Journal d'exécution")

        self.log = tk.Text(bloc_log, height=10, wrap="word")
        self.log.pack(fill="x", padx=5, pady=5)

        # champs
        bloc_champs  = MLFrame(root, text="Résultats")
    
        frame_val = tk.Frame(bloc_champs.content)
        frame_val.pack(fill="none", padx=10, pady=10)

        self.champs = {
            "Date": 20,
            "N° compte": 20,
            "Excel": 20,
            "Nb ope": 10,
            "Dern. ": 98,
            "Erreur" :98
        }
        nbcol = len(self.champs)-2
        r=0
        self.dict_champs = {}                   # dictionnaire des champs réutilisé dans gui_update
        for i, champ in enumerate(self.champs):
            frame = tk.Frame(frame_val)

            label = tk.Label(frame, text=champ)
            label.pack(expand=False, side='left', fill='x', anchor='e', padx=5, pady=2)
     
            field = tk.Entry(frame, width=self.champs[champ])
            field.pack(expand=True, side='left', fill='x', anchor='w', padx=5, pady=2)
            field.configure(justify='center')

            self.dict_champs[champ]=field       # initialisation du dictionnaire dict_champs
            if i < nbcol:
                frame.grid(row=r, column=i, padx=5, pady=5)
            else:
                r += 1
                frame.grid(row=r, column=0, columnspan=nbcol, padx=5, pady=5, sticky='w')
        

        # self.dict_champs["Nb ope"].config(justify="right")
        # self.dict_hamps["Date"].config(justify="center")
            
        # Tableau
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("MonStyle.Treeview", rowheight=row_h)

        bloc_tree = MLFrame(root, text="Opérations bancaires détectées")
     
        self.columns = [
            ('status',  'Status',   0.10, int(80*self.ratio),     False,  'center'),
            ('date',    'Date',     0.10, int(100*self.ratio),    False,  'center'),
            ('libelle', 'Libellé',  0.65, int(0),                 True,   'w'),
            ('montant', 'Montant',  0.15, int(150*self.ratio),    False,  'e'),
        ]

        self.tree = ttk.Treeview(
            bloc_tree.content,
            columns=[name for name, *_ in self.columns],
            show="headings",
            style="MonStyle.Treeview",
        )

        for name, text, percent, min_width, stretch, anchor in self.columns:
            self.tree.heading(name, text=text)
            self.tree.column(name, width=min_width, stretch=stretch, anchor=anchor) # pyright: ignore[reportArgumentType]

        self.tree.pack(fill="both", expand=True, anchor='n', padx=10, pady=10)
        self.tree.bind("<Configure>", self.resize_columns)

        # Boutons
        bloc_buttons = tk.Frame(root)
        
        frame_buttons = tk.Frame(bloc_buttons)
        frame_buttons.pack(padx=10, pady=10)
 
        # bouton Fermeture
        self.btn_close = tk.Button(
            frame_buttons,
            width=20,   # largeur en caractères, pas en pixels
            text="Fermeture",
            state='normal',
            background=GREY,
            font=fontBold,
            command=self.close
        )
        self.btn_close.pack(side='left', padx=5, pady=5, anchor='center')

        # On place les différents blocs dans la fenêtre principale
        bloc_log.grid(      row=0, column=0, sticky="ew",   padx=10, pady=10)
        bloc_champs.grid(   row=1, column=0, sticky="ew",   padx=10, pady=10)
        bloc_tree.grid(     row=2, column=0, sticky="nsew", padx=10, pady=10)
        bloc_buttons.grid(  row=3, column=0, sticky='ew',   padx=10, pady=10)


    def resize_columns(self, event) -> None:
        width_total = event.width
        for row in self.columns:
            name, text, percent, min_width, stretch, anchor = row
            self.tree.column(name, width=max(int(width_total * percent), min_width))
    
    def close(self) -> None:
        self.root.destroy()

    def traitement_erreur(self, entry:tk.Entry):
        entry.configure(background=PINK)

# ============================================================
# GUI update loop
# ============================================================

def gui_update(g: gui, root: tk.Tk):
    # entry = gui.dict_champs["Erreur"]
    # entry.delete(0, 'end')
    # entry.insert(0, root.geometry())
    try:
        while True:
            msg_type, payload = g.gui_queue.get_nowait()

            if msg_type == 'resize':
                g.geometry.pos_left(winmgt.getParentHwnd(root.winfo_id()))
                root.update()
                pass

            elif msg_type == "log":
                g.log.insert("end", payload)
                g.log.see("end")

            elif msg_type == "row":
                g.tree.insert("", "end", values=payload) # payload est un tuple
                g.tree.yview_moveto(1)  # On scroll vers le bas pour voir la dernière ligne ajoutée
            
            elif msg_type == "XL":
                g.oXL = payload

            elif msg_type == 'HTML':
                g.oHTML = payload
            
            elif msg_type == "fnorm":       # Fin normale de la moulinette
                g.voir_Excel=True
               
            else:
                entry = g.dict_champs[msg_type]
                entry.delete(0, 'end')
                entry.insert(0, payload)
                if msg_type == "Erreur":
                    g.traitement_erreur(entry)
                    
    except queue.Empty:
        pass

    root.after(100, gui_update, g, root) # On relance la procédure après 100 msec.
