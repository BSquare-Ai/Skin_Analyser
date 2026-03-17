import cv2

# Dermatology region landmark indices (MediaPipe FaceMesh)
FACE_REGIONS = {
    "forehead": [10, 338, 297, 332],
    "left_cheek": [50, 205, 187, 147],
    "right_cheek": [280, 425, 411, 376],
    "under_eye": [33, 133, 159, 145]
}


# -----------------------------
# Extract skin regions
# -----------------------------
def extract_skin_regions(frame, landmarks):

    h, w, _ = frame.shape

    regions = {}
    boxes = {}

    for name, points in FACE_REGIONS.items():

        xs = []
        ys = []

        for p in points:

            lm = landmarks.landmark[p]

            xs.append(int(lm.x * w))
            ys.append(int(lm.y * h))

        x_min = max(min(xs), 0)
        x_max = min(max(xs), w)

        y_min = max(min(ys), 0)
        y_max = min(max(ys), h)

        if x_max <= x_min or y_max <= y_min:
            regions[name] = None
            boxes[name] = None
            continue

        patch = frame[y_min:y_max, x_min:x_max]

        regions[name] = patch
        boxes[name] = (x_min, y_min, x_max - x_min, y_max - y_min)

    return regions, boxes


# -----------------------------
# Draw region boxes on frame
# -----------------------------
def draw_skin_regions(frame, landmarks):

    h, w, _ = frame.shape

    for name, points in FACE_REGIONS.items():

        xs = []
        ys = []

        for p in points:

            lm = landmarks.landmark[p]

            xs.append(int(lm.x * w))
            ys.append(int(lm.y * h))

        x_min = max(min(xs), 0)
        x_max = min(max(xs), w)

        y_min = max(min(ys), 0)
        y_max = min(max(ys), h)

        if x_max <= x_min or y_max <= y_min:
            continue

        cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (255, 0, 0), 2)

        cv2.putText(
            frame,
            name,
            (x_min, y_min - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 0, 0),
            1
        )

    return frame