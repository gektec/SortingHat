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

                hat_width = int(abs(right_eye.x - left_eye.x) * w * 10)
                hat_height = int(hat_width * self.hat_image.shape[0] / self.hat_image.shape[1])
                hat_resized = cv2.resize(self.hat_image, (hat_width, hat_height))

                x = int(left_eye.x * w - hat_width / 2.4)
                y = int(left_eye.y * h - hat_height / 1)

                y1 = max(0, y)
                y2 = min(h, y + hat_height)
                x1 = max(0, x)
                x2 = min(w, x + hat_width)

                if y2 > y1 and x2 > x1:
                    hat_part = hat_resized[y1-y:y2-y, x1-x:x2-x]
                    alpha_channel = hat_part[:, :, 3] / 255.0
                    inverse_alpha = 1.0 - alpha_channel

                    for c in range(0, 3):
                        image[y1:y2, x1:x2, c] = (image[y1:y2, x1:x2, c] * inverse_alpha +
                                                  hat_part[:, :, c] * alpha_channel)

            self.frame = image

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.running = False

    def get_frame(self):
        return self.frame

    def release(self):
        self.running = False
        self.cap.release()
        self.face_mesh.close()  # 释放mediapipe资源