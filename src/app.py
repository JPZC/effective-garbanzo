import time

from src.commands import CommandProcessor
from src.voice import VoiceListener


def main() -> None:
    processor = CommandProcessor()
    listener = VoiceListener()

    print("Asistente listo. Di un comando en español...")

    while True:
        try:
            text = listener.listen()
        except RuntimeError as exc:
            print(str(exc))
            break
        except KeyboardInterrupt:
            print("Saliendo...")
            break

        if not text:
            continue

        print(f"Reconocido: {text}")
        response = processor.handle(text)
        print(response)
        time.sleep(0.3)


if __name__ == "__main__":
    main()
