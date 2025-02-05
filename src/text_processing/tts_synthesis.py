import pyttsx3

class TTSSynthesis:
    def __init__(self):
        self.engine = pyttsx3.init()

    def synthesize_speech(self, text):
        self.engine.say(text)
        self.engine.runAndWait()
