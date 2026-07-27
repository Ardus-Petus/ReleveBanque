import os
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from ReleveBanque.utils import chrome
os.environ['WDM_LOCAL'] = '0'
os.environ['WDM_SSL_VERIFY'] = '0'

class HTML:
    def __init__(self, url:str, test_stop:function):
        self.rows = None    # Liste des lignes du tableau HTML
        self.test_stop = test_stop # Procédure à appeler pour tester le flag de stop
        obj = chrome.ChromeDriver(url)
        self.proc = obj.proc
        self.driver = obj.driver
            
    def quit(self) -> None:
        """Ferme proprement Selenium et le processus Chrome associé."""
        self.driver.quit()
        self.proc.terminate()
        self.proc.wait()

    
    def WaitFor(self, url: str, delay: int) -> bool:
        """
        Attend que l'URL corresponde à `url`, pendant `delay` secondes.
        Interruption immédiate si stop_event est activé.
        Retourne True si l'URL est atteinte, False si stop_event est activé.
        """

        condition = WaitOrStop(self.test_stop, EC.url_matches(url))
        WebDriverWait(self.driver, delay).until(condition)
    
class WaitOrStop:
    def __init__(self, test_stop:function, condition):
        self.test = test_stop      # procedure
        self.condition = condition        # fonction Selenium (driver) -> bool

    def __call__(self, driver):
        # Interruption immédiate 
        if self.test: self.test()                         # Lève éventuellement une exception
        # On délègue à la vraie condition
        return self.condition(driver)

