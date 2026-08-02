import os
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from ReleveBanque.utils import chrome
from ReleveBanque.core.Ope import Ope
from abc import ABC, abstractmethod

os.environ['WDM_LOCAL'] = '0'
os.environ['WDM_SSL_VERIFY'] = '0'

BY_XPATH = By.XPATH

class HTML(ABC):
    def __init__(self, url:str=''):
        self.rows = None    # Liste des lignes du tableau HTML
        self.chrome = chrome.ChromeDriver(url)
        self.proc = self.chrome.proc
        self.driver = self.chrome.driver
            
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

    def findElement(self, value: str) -> WebElement:
        return self.driver.find_element(BY_XPATH, value)

    def findElements(self, value: str) -> list[WebElement]:
        return self.driver.find_elements(BY_XPATH, value)

    def findCells(self, row: WebElement) -> list[WebElement]:
        return row.find_elements(BY_XPATH, './td')

    @abstractmethod
    def waitForRelevé(self) -> None:                        # Initialise le tableau self.rows avec la liste des opérations,
        pass

    @abstractmethod
    def waitForCnxComptes(self) -> None:
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

