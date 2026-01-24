import cv2

def qr_code_scanner():
    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()

    print("Scanning QR... Press 'q' to exit")

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        data, bbox, _ = detector.detectAndDecode(frame)

        cv2.imshow("QR Code Scanner", frame)

        if data:
            cap.release()
            cv2.destroyAllWindows()
            # print(data.strip())
            return data.strip()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return None
