# main_LBP.py
import threading
import queue
import tkinter as tk
from typing import Any
from ReleveBanque.core.modgui import gui, gui_update            # GUI
from ReleveBanque.core.application import Application           # Application
from ReleveBanque.utils.geometry import Geometry

# Queues
gui_queue : queue.Queue[tuple[str, Any]]= queue.Queue()
metier_queue : queue.Queue[tuple[str, Any]]= queue.Queue()

class Lanceur:
    def __init__(self, f_Excel:type, f_HTML:type):
        self.f_Excel = f_Excel
        self.f_HTML = f_HTML
        self.geo = Geometry()

    def main(self):
        # Création de la fenêtre Tkinter
        root = tk.Tk()

        # Instanciation du GUI (modgui.py)
        mygui = gui(root, gui_queue, metier_queue, self.geo)

        # Lancement de l'application dans un thread
        t = threading.Thread(target=self.lancer_moulinette, daemon=True)
        t.start()

        # Affichage du GUI dans le Thread principal
        gui_queue.put(('resize', None))
        root.after(100, gui_update, mygui, root)
        root.mainloop()

        if mygui.oHTML:
            mygui.oHTML.quit()

        if mygui.oXL:
            mygui.oXL.mgr.maximize()

    def lancer_moulinette(self):
        """Lance l'application métier dans un thread."""
        pass
        app = Application(
            mod_XL=self.f_Excel,
            mod_HTML=self.f_HTML,
            gui_queue=gui_queue,                                                                        
            metier_queue=metier_queue,
            geo=self.geo
        )
        app.main()
