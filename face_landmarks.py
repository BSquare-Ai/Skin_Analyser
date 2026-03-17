import mediapipe as mp
import numpy as np
import cv2

mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True
)

def get_face_landmarks(image):

    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    results = face_mesh.process(rgb)

    if not results.multi_face_landmarks:
        return None

    face_landmarks = results.multi_face_landmarks[0]

    points = []

    h, w, _ = image.shape

    for lm in face_landmarks.landmark:

        x = int(lm.x * w)
        y = int(lm.y * h)
        z = lm.z

        points.append([x, y, z])

    return np.array(points)