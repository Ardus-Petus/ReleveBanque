import win32gui

def list_excel_windows():
    """Retourne toutes les fenêtres XLMAIN avec leur titre."""
    hwnds = []

    def enum_handler(hwnd, lParam):
        if win32gui.GetClassName(hwnd) == "XLMAIN":
            title = win32gui.GetWindowText(hwnd)
            hwnds.append((hwnd, title))
        return True

    win32gui.EnumWindows(enum_handler, None)
    return hwnds


def get_hwnd_for_workbook(target_name):
    """
    Retourne le HWND de la fenêtre Excel affichant target_name.
    target_name : nom du fichier (ex: '3438032G033.xlsx')
    """
    target_name = target_name.lower()

    for hwnd, title in list_excel_windows():
        if not title:  # fenêtre XLMAIN "mère" sans titre
            continue

        # Exemple de titre : "3438032G033.xlsx - Excel"
        if target_name in title.lower():
            return hwnd

    return None
