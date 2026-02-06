import cv2
import numpy as np

def decode_qr_from_image(image_bytes):
    """
    Decodes QR code data from image bytes captured via Streamlit camera_input.
    Works on:
    - Streamlit Cloud
    - Local browser
    - Mobile browser
    """
    try:
        np_img = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

        detector = cv2.QRCodeDetector()
        data, _, _ = detector.detectAndDecode(img)

        return data.strip() if data else None
    except Exception:
        return None
