import cv2
import numpy as np

def extract_first_frame(video_bytes):
    nparr = np.frombuffer(video_bytes, np.uint8)
    cap = cv2.VideoCapture(cv2.imdecode(nparr, cv2.IMREAD_COLOR))
    ret, frame = cap.read()
    if ret:
        return frame
    return None
