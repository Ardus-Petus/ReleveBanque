# application.py
import queue
import locale
import pythoncom
import traceback
from datetime import datetime
from importlib import resources

from ReleveBanque.utils import winmgt
from ReleveBanque.utils.geometry import Geometry
from ReleveBanque.core.extraction_metier import ExtractionMetier

class Application:
    """Module principal de l'application Moulinette."""

    def __init__(self, mod_XL:type, mod_HTML:type, gui_queue:queue.Queue, metier_queue:queue.Queue, geo:Geometry):
        self.gui_queue = gui_queue            
        self.metier_queue = metier_queue
        self.mod_XL = mod_XL
        self.mod_HTML = mod_HTML
        self.geometry = geo
        self.tabexcl = self.load_exclusions()

    def main(self):
        pythoncom.CoInitialize()
        #os.chdir(os.path.dirname(__file__))
        locale.setlocale(locale.LC_ALL, 'fr_FR')

        self.putGUI("Date", datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

        metier = ExtractionMetier(self.mod_XL, self.mod_HTML, self.tabexcl)

        try:
            metier.run(callback=self.putGUI)
        except Exception as err:
            with open('.\\ftrace.txt', 'w') as dump:
                dump.write(traceback.format_exc())
            self.putGUI("log", "Fin anormale du programme")
            self.putGUI("Erreur", f"{err.__class__.__name__} : {err}")
        finally:
            if metier.oHTML:
                metier.oHTML.quit()

        return True

    def load_exclusions(self):
        excl = resources.files(self.mod_XL.__module__).joinpath("exclusions.txt").read_text()
        return excl

    def putGUI(self, msg_type, payload):
        # réactions côté présentation
        if msg_type == "html_opened":
            pid = payload
            hwnd_html = winmgt.getChromeWindowFromPid(pid)
            self.geometry.pos_right(hwnd_html)
            winmgt.focus(hwnd_html)
            return

        elif msg_type == "XL_opened":
            oXL = payload
            hwnd_excel = oXL.hwnd
            self.geometry.pos_right(hwnd_excel)
            
        else:       
            # transmettre directement au GUI
            self.gui_queue.put((msg_type, payload))

 