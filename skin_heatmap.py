import cv2
import numpy as np


def draw_skin_heatmap(frame, regions, region_health, boxes):

    heat_mask = np.zeros(frame.shape[:2], dtype=np.uint8)
    face_mask = np.zeros(frame.shape[:2], dtype=np.uint8)

    if not boxes:
        return frame

    h_frame, w_frame = frame.shape[:2]

    for region_name, (x, y, w, h) in boxes.items():

        score = region_health.get(region_name, 50)

        x = max(0, min(int(x), w_frame - 1))
        y = max(0, min(int(y), h_frame - 1))
        w = max(1, min(int(w), w_frame - x))
        h = max(1, min(int(h), h_frame - y))

        value = int(np.interp(score, [50, 80], [50, 255]))

        center_x = x + w // 2
        center_y = y + h // 2
        radius = max(w, h) // 2

        cv2.circle(heat_mask, (center_x, center_y), radius, value, -1)
        cv2.circle(face_mask, (center_x, center_y), radius, 255, -1)

    heatmap = cv2.applyColorMap(heat_mask, cv2.COLORMAP_TURBO)

    face_mask_3ch = cv2.merge([face_mask, face_mask, face_mask])

    background = cv2.bitwise_and(frame, cv2.bitwise_not(face_mask_3ch))
    heat_applied = cv2.bitwise_and(heatmap, face_mask_3ch)

    face_combined = cv2.addWeighted(frame, 0.7, heat_applied, 0.3, 0)

    output = cv2.add(background, face_combined)

    return output