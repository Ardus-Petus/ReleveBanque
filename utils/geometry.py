# geometry.py
from ReleveBanque.utils import winmgt
import ctypes
from win32api import GetMonitorInfo, MonitorFromPoint
class Geometry:
    def __init__(self):
        ctypes.windll.user32.SetProcessDpiAwarenessContext(-4)  # PER_MONITOR_AWARE_V2
        rect = GetMonitorInfo(MonitorFromPoint((0,0)))['Work']  # Dimension de l'écran sans compter la TaskBar
        _, _, self.screen_width, self.screen_height =  rect
        self.mid_x = self.screen_width * 1 // 2
        self.mid_w = self.screen_width - self.mid_x
        self.margin = 0
        self.bordure = 0

    def pos_right(self, hwnd: int):
        # winmgt.maximize(hwnd)
        winmgt.setWindowPos(
            hwnd=hwnd,
            x=self.mid_x + self.margin - self.bordure,
            y=self.margin - self.bordure,
            w=self.mid_w - 2 * self.margin + 2 * self.bordure,
            h=self.screen_height - 2 * self.margin + 2 * self.bordure
        )

    def pos_left(self, hwnd:int):
        # winmgt.maximize(hwnd)
        winmgt.setWindowPos(
            hwnd=hwnd,
            x=self.margin - self.bordure,
            y=self.margin - self.bordure,
            w=self.mid_w - 2 * self.margin + 2 * self.bordure,
            h=self.screen_height - 2 * self.margin + 2 * self.bordure
        )

