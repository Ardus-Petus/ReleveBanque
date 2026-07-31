import os
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from ReleveBanque.utils import chrome
from ReleveBanque.core.Ope import Ope
from abc import ABC, abstractmethod

os.environ['WDM_LOCAL'] = '0'
os.environ['WDM_SSL_VERIFY'] = '0'

class HTML(ABC):
    def __init__(self, url:str=''):
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

    # Méthodes qui doivent être implémentées dans une classe dérivée
    @abstractmethod
    def waitForCnxComptes(self) -> None:
        pass

    @abstractmethod
    def waitForRelevé(self) -> None:                        # Initialise le tableau self.rows avec la liste des opérations,
        pass
    
    @abstractmethod
    def getAcctNo(self) -> str:
        pass

    @abstractmethod
    def getSolde(self) -> float:
        pass

    @abstractmethod
    def getHTMLOpe(self, i: int) -> Ope:
        pass

