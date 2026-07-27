import os
import subprocess
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
os.environ['WDM_LOCAL'] = '0'
os.environ['WDM_SSL_VERIFY'] = '0'
from webdriver_manager.chrome import ChromeDriverManager
import urllib3

CHROMEPROFILE = 'O:\\selenium\\chromeprofile'
CHROMEEXE = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

class ChromeDriver():

    def __init__(self,url:str):
        """Classe pour ouvrir Chrome avec un Webdriver."""
        """Initialise le navigateur et le WebDriver"""                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
        exe = CHROMEEXE
        port_num = "9222"
        port_arg = f'--remote-debugging-port={port_num}'
        userdata = f'--user-data-dir={CHROMEPROFILE}'
        
        # === 1. FORCE LA RÉINITIALISATION DU FLAG DE CRASH ===
        prefs_path = os.path.join(CHROMEPROFILE, 'Default', 'Preferences')
        if os.path.exists(prefs_path):
            try:
                import json
                with open(prefs_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # On force les valeurs de sortie propre pour éviter la bulle "Restaurer"
                if 'profile' in data:
                    data['profile']['exit_type'] = "Normal"
                    data['profile']['exited_cleanly'] = True
                
                with open(prefs_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f)
            except Exception as e:
                print(f"Note: Impossible de réinitialiser le flag de crash ({e})")

        # === 2. ARGUMENTS POUR DEMARRER SANS LES ANCIENS ONGLETS ===
        args = [
            exe, 
            url,
            port_arg, 
            userdata,
            '--disable-session-crashed-bubble',
            '--no-first-run',
            # On demande explicitement à Chrome d'ignorer la session précédente
            '--incognito' if False else '', # Optionnel : si un jour vous voulez du mode privé
        ]
        # Supprime les arguments vides s'il y en a
        args = [arg for arg in args if arg]
        
        self.proc = subprocess.Popen(
            args,
            creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0
        )
        
        # On laisse 1 secondes à Chrome pour ouvrir l'interface et le port réseau
        time.sleep(1) 
        urllib3.disable_warnings()
        option = Options()
        option.debugger_address = f"127.0.0.1:{port_num}"
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=option)
        except Exception as e:
            self.proc.terminate()
            raise e
        
