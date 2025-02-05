import sys
import threading
import time
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtCore import QTimer, Qt, Q_ARG, QMetaObject

# 可二选一
from src.text_processing.deepseek_api import OpenAIAPI
#from src.text_processing.openai_api import OpenAIAPI

from src.text_processing.tts_synthesis import TTSSynthesis
from src.video_processing import VideoProcessing
from src.threading_utils import ThreadManager
from src.pyqt_utils import PyQtDisplay, InputBox, LogDisplay

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._setup_ui()
        self._init_resources()
        self._setup_connections()
        self._start_initial_processes()

    def _setup_ui(self):
        self.setWindowTitle("Sorting Hat")
        self.setGeometry(100, 100, 1280, 720)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        main_layout = QVBoxLayout(self.central_widget)
        self.pyqt_display = PyQtDisplay()
        self.log_display = LogDisplay(self)
        self.input_box = InputBox(100, 600, 400, 40, "Enter your text...", self)

        main_layout.addWidget(self.pyqt_display)
        main_layout.addWidget(self.log_display)
        main_layout.addWidget(self.input_box)

    def _init_resources(self):
        self.exit_requested = False
        self.exit_lock = threading.Lock()
        self.cumulative_scores = {"Gryffindor": 0, "Hufflepuff": 0, 
                                "Ravenclaw": 0, "Slytherin": 0}
        
        self.openai_api = OpenAIAPI()
        self.tts_synthesis = TTSSynthesis()
        self.video_processing = VideoProcessing()
        self.thread_manager = ThreadManager()

    def _setup_connections(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.input_box.input.returnPressed.connect(self.handle_input_box)
        self.input_box.button.clicked.connect(self.handle_input_box)

    def _start_initial_processes(self):
        self.thread_manager.start_thread(self.video_processing.process_video)
        self.timer.start(30)
        
        initial_prompt = "Welcome to Hogwarts. Let me piken in thine soule..."
        self._log_and_speak(initial_prompt, is_user=False)

    def handle_input_box(self):
        if user_input := self.input_box.input.text().strip():
            self.input_box.input.clear()
            self._log_and_speak(user_input, is_user=True)
            threading.Thread(
                target=self.process_user_input,
                args=(user_input,),
                daemon=True
            ).start()

    def process_user_input(self, user_input):
        response = self.openai_api.process_text(user_input)
        self._update_interface(response)
        self._update_scores(response)
        self._check_exit_condition()

    def _update_interface(self, response):
        QMetaObject.invokeMethod(self.log_display, "append",
                               Qt.ConnectionType.QueuedConnection,
                               Q_ARG(str, f"Sorting Hat: {response.hat_response}"))
        self.tts_synthesis.synthesize_speech(response.hat_response)

    def _update_scores(self, response):
        for house in self.cumulative_scores:
            self.cumulative_scores[house] += getattr(response, house.lower())

    def _check_exit_condition(self):
        if any(score > 15 for score in self.cumulative_scores.values()):
            winner = max(self.cumulative_scores, key=self.cumulative_scores.get)
            exit_prompt = f"In accordance wyth thyne soul, thou shouldst be allotted to {winner}."
            self._log_and_speak(exit_prompt, is_user=False)
            time.sleep(3)
            
            with self.exit_lock:
                self.exit_requested = True

    def update_frame(self):
        with self.exit_lock:
            if self.exit_requested:
                self.close()
                return
        self.pyqt_display.update_display(self.video_processing.get_frame())

    def _log_and_speak(self, message, is_user=True):
        prefix = "You" if is_user else "Sorting Hat"
        self.log_display.append(f"{prefix}: {message}")
        if not is_user:
            threading.Thread(
                target=self.tts_synthesis.synthesize_speech,
                args=(message,),
                daemon=True
            ).start()

    def closeEvent(self, event):
        self.timer.stop()
        self.thread_manager.stop_all_threads()
        self.video_processing.release()
        
        # Cleanup TTS resources if needed
        if hasattr(self.tts_synthesis, 'cleanup'):
            self.tts_synthesis.cleanup()
            
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())