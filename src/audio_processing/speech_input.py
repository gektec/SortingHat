import speech_recognition as sr
import queue

class SpeechInput:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.audio_queue = queue.Queue()

    def get_speech(self):
        with sr.Microphone() as source:
            print("请说话...")
            audio = self.recognizer.listen(source)
            try:
                text = self.recognizer.recognize_google(audio, language="zh-CN")
                print(f"你说的是: {text}")
                return text
            except sr.UnknownValueError:
                print("无法识别语音")
            except sr.RequestError:
                print("请求失败")
        return None
