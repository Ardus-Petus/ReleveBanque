import os
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from ReleveBanque.utils import chrome
os.environ['WDM_LOCAL'] = '0'
os.environ['WDM_SSL_VERIFY'] = '0'

class HTML:
    def __init__(self, url:str):
        self.rows = None    # Liste des lignes du tableau HTML
        obj = chrome.ChromeDriver(url)
        self.proc = obj.proc
        self.driver = obj.driver
            
    def quit(self) -> None:
        """Ferme proprement Selenium et le processus Chrome associé."""
        #self.driver.quit()
        self.proc.terminate()
        self.proc.wait()

    
    def WaitFor(self, url: str, delay: int) -> None:
        """
        Attend que l'URL corresponde à `url`, pendant `delay` secondes.
        Interruption immédiate si stop_event est activé.
        Retourne True si l'URL est atteinte, False si stop_event est activé.
        """

        WebDriverWait(self.driver, delay).until(EC.url_matches(url))
    
