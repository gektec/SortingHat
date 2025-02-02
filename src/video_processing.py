import cv2
import mediapipe as mp
import numpy as np

class VideoProcessing:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5)
        self.hat_image = cv2.imread('assets/hat.png', -1)  # 带有alpha通道
        self.cap = cv2.VideoCapture(0)
        self.frame = None
        self.running = True

    def process_video(self):
        while self.running:
            success, image = self.cap.read()
            if not success:
                break

            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = self.face_mesh.process(image_rgb)

            if results.multi_face_landmarks:
                face_landmarks = results.multi_face_landmarks[0]
                h, w, _ = image.shape

                left_eye_idx = 133
                right_eye_idx = 362
                left_eye = face_landmarks.landmark[left_eye_idx]
                right_eye = face_landmarks.landmark[right_eye_idx]

                hat_width = int(abs(right_eye.x - left_eye.x) * w * 3)
                hat_height = int(hat_width * self.hat_image.shape[0] / self.hat_image.shape[1])
                hat_resized = cv2.resize(self.hat_image, (hat_width, hat_height))
                x = int(left_eye.x * w - hat_width / 4)
                y = int(left_eye.y * h - hat_height / 1.2)

                for i in range(hat_height):
                    for j in range(hat_width):
                        if hat_resized[i, j][3] != 0:
                            offset_y = y + i
                            offset_x = x + j
                            if offset_x < w and offset_y < h:
                                image[offset_y, offset_x] = hat_resized[i, j][:3]

            self.frame = image

    def get_frame(self):
        return self.frame

    def release(self):
        self.running = False
        self.cap.release()
