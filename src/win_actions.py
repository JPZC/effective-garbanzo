import subprocess
import time
from pathlib import Path

import pyautogui


class DesktopActions:
    def open_app(self, name: str) -> None:
        subprocess.Popen(["cmd", "/c", "start", "", name], shell=False)

    def open_path(self, path: str) -> None:
        resolved = Path(path).expanduser()
        subprocess.Popen(["cmd", "/c", "start", "", str(resolved)], shell=False)

    def click(self, x: int, y: int, right_click: bool = False) -> None:
        pyautogui.moveTo(x, y, duration=0.1)
        if right_click:
            pyautogui.click(button="right")
        else:
            pyautogui.click()

    def type_text(self, text: str) -> None:
        time.sleep(0.2)
        pyautogui.write(text, interval=0.02)
