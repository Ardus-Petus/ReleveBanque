import time
import win32gui
import win32con
import win32api
import win32process 
import ctypes
import pyautogui

# Récupération de la résolution de l'écran
# ---------------------------------------------------------
def get_screen_size() -> tuple[int, int]:
    w = win32api.GetSystemMetrics(0)
    h = win32api.GetSystemMetrics(1)
    return w, h

# Récupération du HWND de la fenêtre active et renommage
# ---------------------------------------------------------
def getCurrentHwnd() -> int:
    hwnd_potentiel = win32gui.GetForegroundWindow()
    jeton_unique = f"New_Window_{time.time()}"
    win32gui.SetWindowText(hwnd_potentiel, jeton_unique) #type: ignore
    time.sleep(0.02)
    hwnd_console = win32gui.FindWindow(None, jeton_unique)
    return hwnd_console

# Positionnement et redimensionnement de la fenêtre
# ---------------------------------------------------------
def setWindowPos(hwnd: int, x: int, y: int, w: int, h: int) -> None:
    win32gui.SetWindowPos(
        hwnd, win32con.HWND_TOP, 
        x, y, w, h, 
        win32con.SWP_SHOWWINDOW
    )
    pass

# Fermeture forcée de la fenêtre via Windows
# ---------------------------------------------------------
def close_window(hwnd: int) -> None:
    #Envoie un message WM_CLOSE à la fenêtre spécifiée pour la fermer.
    # WM_CLOSE (0x0010) force la fenêtre Windows à se détruire immédiatement
    # ce qui ferme le prompt système.
    win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
 
# Récupérer le HWND d’un processus *
# ---------------------------------------------------------
def getChromeWindowFromPid(pid: int) -> int:
    hwnds:list[int] = []

    def callback(hwnd: int, _):
        # Vérifie le PID
        _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
        if found_pid != pid:
            return True

        # Fenêtre visible
        if not win32gui.IsWindowVisible(hwnd):
            return True

        # Fenêtre racine (évite les enfants)
        root = win32gui.GetAncestor(hwnd, win32con.GA_ROOT)
        if root != hwnd:
            return True

        hwnds.append(hwnd)
        return True

    # Chrome peut mettre longtemps à afficher sa fenêtre
    for _ in range(60):  # 6 secondes
        win32gui.EnumWindows(callback, None)
        if hwnds:
            break
        time.sleep(0.1)

    if not hwnds:
        raise ValueError(f"Aucune fenêtre Chrome trouvée pour le PID {pid}.")
    if len(hwnds) > 1:
        raise ValueError(f"Plusieurs fenêtres Chrome trouvées pour le PID {pid}.")
    return hwnds[0]

# Réduire la fenêtre
# ---------------------------------------------------------
def minimize(hwnd: int)-> None:
    win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)

# Restaurer la fenêtre
# --------------------------------------------------------- 
def restore(hwnd: int)-> None:
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE) 

# Maximiser la fenêtre
# ---------------------------------------------------------     
def maximize(hwnd: int)-> None: 
    win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)

def focus(hwnd: int) -> None:
    # Force la fenêtre à passer au premier plan
    # Source - https://stackoverflow.com/a/76386100
    # Posted by crxyz
    # Retrieved 2026-06-05, License - CC BY-SA 4.0

    pyautogui.press("alt")

    win32gui.SetForegroundWindow(hwnd)
    win32gui.BringWindowToTop(hwnd)

def getParentHwnd(hwndTk: int) -> int:
    # Récupération du a HWND parent
    return ctypes.windll.user32.GetParent(hwndTk)
