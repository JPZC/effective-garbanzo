import speech_recognition as sr


class VoiceListener:
    def __init__(self, language: str = "es-ES") -> None:
        self.recognizer = sr.Recognizer()
        self.language = language

    def listen(self) -> str:
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = self.recognizer.listen(source)

        try:
            return self.recognizer.recognize_google(audio, language=self.language)
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            return ""
