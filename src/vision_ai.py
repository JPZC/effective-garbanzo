import base64
import os
from dataclasses import dataclass
from typing import Optional, Tuple

import mss
import numpy as np
import requests


@dataclass
class DetectedObject:
    x: int
    y: int
    score: float


class VisionAIHelper:
    def __init__(self, model: str = "google/owlvit-base-patch32") -> None:
        self.model = model
        self.api_url = f"https://api-inference.huggingface.co/models/{model}"
        self.api_token = os.getenv("HF_API_TOKEN")

    def find_object_by_text(self, query: str) -> Optional[Tuple[int, int]]:
        screenshot = self._capture_screen()
        detection = self._query_inference_api(query, screenshot)
        if not detection:
            return None

        return detection.x, detection.y

    def _capture_screen(self) -> np.ndarray:
        with mss.mss() as screen:
            monitor = screen.monitors[1]
            shot = screen.grab(monitor)
            image = np.array(shot)
        return image

    def _query_inference_api(self, query: str, screenshot: np.ndarray) -> Optional[DetectedObject]:
        encoded = self._encode_image(screenshot)
        payload = {
            "inputs": {
                "image": encoded,
                "text_queries": [query],
            }
        }
        headers = {}
        if self.api_token:
            headers["Authorization"] = f"Bearer {self.api_token}"

        response = requests.post(self.api_url, json=payload, headers=headers, timeout=60)
        if response.status_code != 200:
            return None

        data = response.json()
        if not data:
            return None

        best = max(data, key=lambda item: item.get("score", 0.0))
        if best.get("score", 0.0) < 0.4:
            return None

        box = best.get("box") or {}
        x = int((box.get("xmin", 0) + box.get("xmax", 0)) / 2)
        y = int((box.get("ymin", 0) + box.get("ymax", 0)) / 2)
        return DetectedObject(x=x, y=y, score=float(best.get("score", 0.0)))

    @staticmethod
    def _encode_image(image: np.ndarray) -> str:
        import cv2

        success, buffer = cv2.imencode(".png", image)
        if not success:
            return ""
        return base64.b64encode(buffer).decode("utf-8")
