# effective-garbanzo

Asistente de voz para Windows 11 con control del escritorio y visión (captura de pantalla) para ejecutar acciones como abrir apps, archivos, carpetas y realizar clics guiados por lo que ves.

## Funcionalidades

- **Comandos de voz en español** para abrir aplicaciones, archivos y carpetas.
- **Visión por IA (sin plantillas)**: detección por texto usando un modelo gratuito (Hugging Face Inference API).
- **Visión por plantillas**: alternativa local con template matching.
- **Acciones de escritorio** (clic, doble clic, clic derecho, escribir texto).

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

Instala todo con:

```bash
pip install -r requirements.txt
```

> Nota: En Windows, `pyaudio` puede requerir instalar un wheel compatible.

## Uso rápido

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

## Cómo funciona la visión por IA

Se toma una captura de pantalla y se envía a la **Hugging Face Inference API** usando un modelo de detección por texto (`google/owlvit-base-patch32`). El modelo devuelve la caja del elemento que mejor coincide con lo que dices (por ejemplo, "icono de chrome") y se hace clic en el centro.

## Estructura

```
.
├── README.md
├── requirements.txt
├── templates/
└── src/
    ├── app.py
    ├── commands.py
    ├── vision.py
    ├── vision_ai.py
    ├── voice.py
    └── win_actions.py
```

## Notas de seguridad

Este proyecto automatiza acciones del escritorio. Revísalo y ajústalo a tu entorno antes de usarlo en un equipo con información sensible.
