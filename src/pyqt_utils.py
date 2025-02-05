from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt, QTimer
import cv2

class PyQtDisplay(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 1280, 720)
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.window_width, self.window_height = 1280, 720

    def update_display(self, frame):
        if frame is not None:
            # 计算视频的原始宽高比
            original_height, original_width = frame.shape[:2]
            aspect_ratio = original_width / original_height
            
            # 计算视频在窗口上半部分的高度
            target_height = self.window_height // 2
            
            # 根据宽高比计算目标宽度
            target_width = int(target_height * aspect_ratio)
            
            # 调整视频大小，保持宽高比
            frame_resized = cv2.resize(frame, (target_width, target_height))
            
            # 将视频转换为RGB格式并转换为QImage对象
            frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
            h, w, ch = frame_rgb.shape
            bytes_per_line = ch * w
            q_img = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
            
            # 计算视频在窗口上半部分的居中位置
            x_offset = (self.window_width - target_width) // 2
            
            # 将视频绘制到窗口的上半部分并更新显示
            self.label.setPixmap(QPixmap.fromImage(q_img))
            self.label.setGeometry(x_offset, 0, target_width, target_height)

class InputBox(QWidget):
    def __init__(self, x, y, w, h, text='', parent=None):
        super().__init__(parent)
        self.setGeometry(x, y, w, h)
        self.layout = QHBoxLayout()
        
        self.input = QLineEdit(self)
        self.input.setPlaceholderText(text)
        self.input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #10263B;
                border-radius: 5px;
                padding: 5px;
                font-size: 16px;
            }
            QLineEdit:focus {
                border: 2px solid #405162;
            }
        """)
        
        self.button = QPushButton(" Enter ", self)
        self.button.setStyleSheet("""
            QPushButton {
                background-color: #9FA8B1;
                padding: 8px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #707D89;
            }
        """)
        
        self.layout.addWidget(self.input)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

class LogDisplay(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setStyleSheet("""
            QTextEdit {
                border: 2px solid #10263B;
                border-radius: 5px;
                padding: 5px;
                font-size: 16px;
            }
        """)
