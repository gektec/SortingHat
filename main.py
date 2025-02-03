import sys
import threading
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout
from PyQt6.QtCore import QTimer, pyqtSignal, QObject
from src.audio_processing.speech_input import SpeechInput
from src.audio_processing.openai_api import OpenAIAPI
from src.audio_processing.tts_synthesis import TTSSynthesis
from src.video_processing import VideoProcessing
from src.threading_utils import ThreadManager
from src.pyqt_utils import PyQtDisplay, InputBox, LogDisplay

class Communicate(QObject):
    user_input_signal = pyqtSignal(str)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hogwarts Sorting Hat")
        self.setGeometry(100, 100, 1280, 720)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.pyqt_display = PyQtDisplay()
        self.layout.addWidget(self.pyqt_display)

        # 创建日志显示区
        self.log_display = LogDisplay(self)
        self.layout.addWidget(self.log_display)

        self.input_box = InputBox(100, 600, 400, 40, "Enter your text...", self)
        self.layout.addWidget(self.input_box)

        self.exit_requested = False
        self.exit_lock = threading.Lock()
        self.cumulative_scores = {"Gryffindor": 0, "Hufflepuff": 0, "Ravenclaw": 0, "Slytherin": 0}

        self.speech_input = SpeechInput()
        self.openai_api = OpenAIAPI()
        self.tts_synthesis = TTSSynthesis()
        self.video_processing = VideoProcessing()
        self.thread_manager = ThreadManager()
        
        self.comm = Communicate()
        self.comm.user_input_signal.connect(self.process_user_input)
        
        self.thread_manager.start_thread(self.video_processing.process_video)

        self.initial_prompt = "Welcome to Hogwarts. Let me piken in thine soule..."
        print(self.initial_prompt)
        self.tts_synthesis.synthesize_speech(self.initial_prompt)  # 使用TTS读出提示
        
        self.thread_manager.start_thread(self.speech_input_thread)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # 每30ms更新一次

        self.input_box.input.returnPressed.connect(self.handle_input_box)
        self.input_box.button.clicked.connect(self.handle_input_box)

    def handle_input_box(self):
        user_input = self.input_box.input.text()
        self.input_box.input.clear()
        self.comm.user_input_signal.emit(user_input)
        self.log_display.append(f"User: {user_input}")

    def process_user_input(self, user_input):
        response = self.openai_api.process_text(user_input)
        
        self.tts_synthesis.synthesize_speech(response.hat_response)  # 使用TTS进行回复
        
        self.cumulative_scores["Gryffindor"] += response.gryffindor
        self.cumulative_scores["Hufflepuff"] += response.hufflepuff
        self.cumulative_scores["Ravenclaw"] += response.ravenclaw
        self.cumulative_scores["Slytherin"] += response.slytherin
        
        print("\nCurrent Scores:")
        for house, score in self.cumulative_scores.items():
            print(f"{house}: {score}")

        # 根据得分判断退出条件
        if any(score > 15 for score in self.cumulative_scores.values()):
            print("\nHouse with highest score:")
            winner = max(self.cumulative_scores, key=self.cumulative_scores.get)
            
            exit_prompt = f"In accordance wyth thyne soul, thou shouldst be allotted to {winner}."
            self.tts_synthesis.synthesize_speech(exit_prompt)
            print(exit_prompt)

            with self.exit_lock:
                self.exit_requested = True
            return 

    def speech_input_thread(self):
        while True:
            with self.exit_lock:
                if self.exit_requested:
                    return

            # 切换为语音输入
            # user_input = self.speech_input.get_speech()
            
            # 等待来自InputBox的用户输入信号
            QTimer.singleShot(0, lambda: None)

    def update_frame(self):
        frame = self.video_processing.get_frame()
        self.pyqt_display.update_display(frame)

    def closeEvent(self, event):
        self.thread_manager.stop_all_threads()
        self.video_processing.release()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
