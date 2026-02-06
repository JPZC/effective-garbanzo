import os
from dataclasses import dataclass

from src.vision import VisionHelper
from src.vision_ai import VisionAIHelper
from src.win_actions import DesktopActions


@dataclass
class CommandResult:
    message: str


class CommandProcessor:
    def __init__(self) -> None:
        self.actions = DesktopActions()
        self.vision = VisionHelper()
        self.vision_ai = VisionAIHelper()

    def handle(self, text: str) -> str:
        normalized = text.strip().lower()

        if normalized.startswith("abre "):
            target = normalized.replace("abre ", "", 1).strip()
            return self._open_target(target).message

        if normalized.startswith("haz click en plantilla "):
            template_name = normalized.replace("haz click en plantilla ", "", 1).strip()
            return self._click_template(template_name, right_click=False).message

        if normalized.startswith("clic derecho en plantilla "):
            template_name = normalized.replace("clic derecho en plantilla ", "", 1).strip()
            return self._click_template(template_name, right_click=True).message

        if normalized.startswith("haz click en objeto "):
            query = normalized.replace("haz click en objeto ", "", 1).strip()
            return self._click_object(query, right_click=False).message

        if normalized.startswith("clic derecho en objeto "):
            query = normalized.replace("clic derecho en objeto ", "", 1).strip()
            return self._click_object(query, right_click=True).message

        if normalized.startswith("escribe "):
            payload = normalized.replace("escribe ", "", 1)
            self.actions.type_text(payload)
            return "Texto escrito."

        if normalized in {"salir", "terminar", "adios"}:
            raise KeyboardInterrupt

        return "Comando no reconocido."

    def _open_target(self, target: str) -> CommandResult:
        downloads = os.path.join(os.path.expanduser("~"), "Downloads")
        if target in {"descargas", "carpeta descargas"}:
            self.actions.open_path(downloads)
            return CommandResult("Abriendo Descargas.")

        self.actions.open_app(target)
        return CommandResult(f"Abriendo {target}.")

    def _click_template(self, template_name: str, right_click: bool) -> CommandResult:
        location = self.vision.find_template_on_screen(template_name)
        if not location:
            return CommandResult("No encontré la plantilla en pantalla.")

        x, y = location
        self.actions.click(x, y, right_click=right_click)
        return CommandResult("Acción realizada.")

    def _click_object(self, query: str, right_click: bool) -> CommandResult:
        location = self.vision_ai.find_object_by_text(query)
        if not location:
            return CommandResult("No encontré el objeto en pantalla.")

        x, y = location
        self.actions.click(x, y, right_click=right_click)
        return CommandResult("Acción realizada.")
