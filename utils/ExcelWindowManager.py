import win32com.client as win32
import win32gui
import win32con
import time
class ExcelWindowManager:
    def __init__(self):
        self.appli, self.excel_was_running = self._get_excel_instance()
        self.saved_state = None
        self.hwnd = None

    # ---------------------------------------------------------
    # Récupération instance Excel + indicateur
    # ---------------------------------------------------------
    def _get_excel_instance(self):
        try:
            app = win32.GetActiveObject("Excel.Application")
            return app, True   # ✔️ Excel existait déjà
        except Exception:
            app = win32.Dispatch("Excel.Application")
            return app, False  # ✔️ Excel vient d'être créé

    # ---------------------------------------------------------     
    # Maximiser la fenêtre
    # ---------------------------------------------------------     
    def maximize(self)-> None: 
       win32gui.ShowWindow(self.hwnd, win32con.SW_RESTORE) 
       time.sleep(0.1)
       win32gui.ShowWindow(self.hwnd, win32con.SW_MAXIMIZE)
       
 