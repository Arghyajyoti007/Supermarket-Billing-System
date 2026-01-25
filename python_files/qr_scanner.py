import cv2

def qr_code_scanner():
    # Initialize camera capture
    # 0 refers to the default webcam
    cap = cv2.VideoCapture(0)

    # Create QRCodeDetector object (OpenCV built-in QR detector)
    detector = cv2.QRCodeDetector()

    print("Scanning QR... Press 'q' to exit")

    # Infinite loop to continuously scan frames
    while True:
        # Read a single frame from the camera
        # ret  -> Boolean flag (True if frame captured successfully)
        # frame -> Image frame captured from the camera
        ret, frame = cap.read()

        # If frame capture fails, skip this iteration
        if not ret:
            continue

        # Detect and decode QR code from the frame
        # data -> Decoded QR content (string)
        # bbox -> Bounding box of QR (if detected)
        # _    -> Straightened QR image (unused here)
        data, bbox, _ = detector.detectAndDecode(frame)

        # Display camera feed
        cv2.imshow("QR Code Scanner", frame)

        # If QR data is detected
        if data:
            # Release camera resource
            cap.release()

            # Close all OpenCV windows
            cv2.destroyAllWindows()

            # Print and return cleaned QR data
            print(data.strip())
            return data.strip()

        # Exit scanner when 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources if loop exits normally
    cap.release()
    cv2.destroyAllWindows()

    # Return None if no QR was scanned
    return None
