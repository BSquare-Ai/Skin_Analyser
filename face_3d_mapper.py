import mediapipe as mp
import numpy as np

mp_face_mesh = mp.solutions.face_mesh

def extract_face_3d_landmarks(image):

    with mp_face_mesh.FaceMesh(
        static_image_mode=True,
        max_num_faces=1,
        refine_landmarks=True
    ) as face_mesh:

        results = face_mesh.process(image)

        if not results.multi_face_landmarks:
            return None

        face_landmarks = results.multi_face_landmarks[0]

        points_3d = []

        for lm in face_landmarks.landmark:
            points_3d.append([lm.x, lm.y, lm.z])

        return np.array(points_3d)