import cv2
import dlib
import numpy as np

class VideoProcessing:
    def __init__(self):
        # Load the pre-trained model for detecting face landmarks
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("assets/shape_predictor_68_face_landmarks.dat")
        self.hat_image = cv2.imread('assets/hat.png', -1)  # Read the hat image with its alpha channel
        self.cap = cv2.VideoCapture(0)
        self.frame = None
        self.running = True

    def process_video(self):
        while self.running:
            success, image = self.cap.read()
            if not success:
                break

            image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = self.detector(image_gray, 0)

            for face in faces:
                landmarks = self.predictor(image_gray, face)
                
                left_eye = landmarks.part(36)  # Using approximate landmarks corresponding to left and right eyes
                right_eye = landmarks.part(45)
                
                h, w, _ = image.shape
                hat_width = int(abs(right_eye.x - left_eye.x) * 4)
                hat_height = int(hat_width * self.hat_image.shape[0] / self.hat_image.shape[1])
                hat_resized = cv2.resize(self.hat_image, (hat_width, hat_height))

                x = int(left_eye.x - hat_width / 3)
                y = int(left_eye.y - hat_height / 1)

                y1 = max(0, y)
                y2 = min(h, y + hat_height)
                x1 = max(0, x)
                x2 = min(w, x + hat_width)

                if y2 > y1 and x2 > x1:
                    hat_part = hat_resized[y1-y:y2-y, x1-x:x2-x]
                    alpha_channel = hat_part[:, :, 3] / 255.0
                    inverse_alpha = 1.0 - alpha_channel

                    for c in range(0, 3):
                        image[y1:y2, x1:x2, c] = ((image[y1:y2, x1:x2, c] * inverse_alpha) +
                                                  (hat_part[:, :, c] * alpha_channel))

            self.frame = image

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.running = False

    def get_frame(self):
        return self.frame

    def release(self):
        self.running = False
        self.cap.release()

