import cv2
import mediapipe as mp
import numpy as np

# 初始化MediaPipe Face Mesh模型
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5)


# 读取帽子图像
hat_image = cv2.imread('assets/hat.png', -1)  # 带有alpha通道

cap = cv2.VideoCapture(0)  # 开启摄像头



while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    # 转换图像颜色空间从BGR到RGB，并进行处理
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(image_rgb)

    if results.multi_face_landmarks:
        face_landmarks = results.multi_face_landmarks[0]
        h, w, _ = image.shape

        # 示意：获取眼睛和眉毛的坐标来定位帽子
        left_eye_idx = 133  # 眼睛一个特定点的索引
        right_eye_idx = 362
        left_eye = face_landmarks.landmark[left_eye_idx]
        right_eye = face_landmarks.landmark[right_eye_idx]

        # 计算帽子的位置和大小
        # 这里需要根据帽子和面部尺寸进行适当的缩放和转换

        # 举例添加帽子（这里应进一步调整）
        hat_width = int(abs(right_eye.x - left_eye.x) * w * 3)
        hat_height = int(hat_width * hat_image.shape[0] / hat_image.shape[1])
        hat_resized = cv2.resize(hat_image, (hat_width, hat_height))
        x = int(left_eye.x * w - hat_width / 4)
        y = int(left_eye.y * h - hat_height / 1.2)

        # 处理帽子透明度
        for i in range(hat_height):
            for j in range(hat_width):
                if hat_resized[i, j][3] != 0:  # alpha 通道不为 0
                    offset_y = y + i
                    offset_x = x + j
                    if offset_x < w and offset_y < h:
                        image[offset_y, offset_x] = hat_resized[i, j][:3]

    # 显示修改后的图像
    cv2.imshow('MediaPipe Face Mesh', image)
    if cv2.waitKey(5) & 0xFF == 27:
        break


cap.release()
