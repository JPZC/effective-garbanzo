from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple

import cv2
import mss
import numpy as np


@dataclass
class VisionMatch:
    x: int
    y: int
    confidence: float


class VisionHelper:
    def __init__(self, templates_dir: str = "templates") -> None:
        self.templates_dir = Path(templates_dir)

    def find_template_on_screen(self, template_name: str) -> Optional[Tuple[int, int]]:
        template_path = self.templates_dir / f"{template_name}.png"
        if not template_path.exists():
            return None

        screenshot = self._capture_screen()
        template = cv2.imread(str(template_path), cv2.IMREAD_COLOR)

        if template is None:
            return None

        match = self._match_template(screenshot, template)
        if not match or match.confidence < 0.85:
            return None

        return match.x, match.y

    def _capture_screen(self) -> np.ndarray:
        with mss.mss() as screen:
            monitor = screen.monitors[1]
            shot = screen.grab(monitor)
            image = np.array(shot)
        return cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

    def _match_template(self, screenshot: np.ndarray, template: np.ndarray) -> Optional[VisionMatch]:
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if max_val <= 0:
            return None

        height, width = template.shape[:2]
        x = int(max_loc[0] + width / 2)
        y = int(max_loc[1] + height / 2)
        return VisionMatch(x=x, y=y, confidence=float(max_val))
