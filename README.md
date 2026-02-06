# effective-garbanzo

Asistente de voz para Windows 11 con control del escritorio y visión (captura de pantalla) para ejecutar acciones como abrir apps, archivos, carpetas y realizar clics guiados por lo que ves.

## Funcionalidades

- **Comandos de voz en español** para abrir aplicaciones, archivos y carpetas.
- **Visión por IA (sin plantillas)**: detección por texto usando un modelo gratuito (Hugging Face Inference API).
- **Visión por plantillas**: alternativa local con template matching.
- **Acciones de escritorio** (clic, doble clic, clic derecho, escribir texto).
- **UI moderna**: panel visual para enviar comandos, ver estado y diseñar flujos.

## Requisitos

- Windows 11
- Python 3.10+

Dependencias principales:

- `speechrecognition` (reconocimiento de voz)
- `pyaudio` (entrada de micrófono)
- `opencv-python` (visión)
- `mss` (captura de pantalla)
- `pyautogui` (automatización)
- `requests` (llamadas HTTP a la API gratuita de visión)
- `fastapi` + `uvicorn` (servidor para la UI)

Instala todo con:

```bash
pip install -r requirements.txt
```

> Nota: En Windows, `pyaudio` puede requerir instalar un wheel compatible.

## Uso rápido (modo voz + terminal)

1. Si usarás **plantillas**, coloca imágenes de referencia en `templates/`.
2. Si usarás **IA**, crea un token gratuito en Hugging Face y exporta la variable:

```bash
set HF_API_TOKEN=TU_TOKEN
```

3. Ejecuta el asistente:

```bash
python -m src.app
```

### Ejemplos de comandos

- "abre google chrome"
- "abre la carpeta descargas"
- "haz click en objeto icono de chrome"
- "clic derecho en objeto carpeta descargas"
- "haz click en plantilla boton_guardar"
- "clic derecho en plantilla menu_contextual"
- "escribe hola mundo"

## UI moderna (modo visual)

Lanza la interfaz visual y controla todo desde el navegador:

```bash
uvicorn src.ui_server:app --reload
```

Luego abre `http://localhost:8000`.

### Inicio rápido en Windows 11 (PowerShell)

1. Instala dependencias y crea el entorno virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Exporta el token de Hugging Face (opcional, solo IA):

```powershell
$env:HF_API_TOKEN="TU_TOKEN"
```

3. Inicia el modo visual:

```powershell
uvicorn src.ui_server:app --reload
```

4. Abre la interfaz en el navegador:

```
http://localhost:8000
```

5. (Opcional) Inicia el modo voz por consola:

```powershell
python -m src.app
```

## Cómo funciona la visión por IA

Se toma una captura de pantalla y se envía a la **Hugging Face Inference API** usando un modelo de detección por texto (`google/owlvit-base-patch32`). El modelo devuelve la caja del elemento que mejor coincide con lo que dices (por ejemplo, "icono de chrome") y se hace clic en el centro.

## Estructura

```
.
├── README.md
├── requirements.txt
├── templates/
├── ui/
│   ├── app.js
│   ├── index.html
│   └── styles.css
└── src/
    ├── app.py
    ├── commands.py
    ├── ui_server.py
    ├── vision.py
    ├── vision_ai.py
    ├── voice.py
    └── win_actions.py
```

## Notas de seguridad

Este proyecto automatiza acciones del escritorio. Revísalo y ajústalo a tu entorno antes de usarlo en un equipo con información sensible.

## Troubleshooting

**Error `ModuleNotFoundError: No module named 'distutils'` en Python 3.12**  
SpeechRecognition puede requerir `distutils` vía PyAudio. Soluciones:

- Instala `setuptools`:

```bash
pip install setuptools
```

- O usa Python 3.11 (recomendado para máxima compatibilidad con PyAudio).
