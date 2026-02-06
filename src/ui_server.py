from pathlib import Path
from typing import Dict

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from src.commands import CommandProcessor


class CommandPayload(BaseModel):
    text: str


class CommandResponse(BaseModel):
    message: str


def create_app() -> FastAPI:
    app = FastAPI(title="Asistente visual")
    processor = CommandProcessor()
    ui_dir = Path(__file__).resolve().parent.parent / "ui"

    app.mount("/ui", StaticFiles(directory=ui_dir), name="ui")

    @app.get("/")
    def index() -> FileResponse:
        return FileResponse(ui_dir / "index.html")

    @app.post("/api/command", response_model=CommandResponse)
    def command(payload: CommandPayload) -> Dict[str, str]:
        message = processor.handle(payload.text)
        return {"message": message}

    return app


app = create_app()
