📷 QR Code Scanner – Methods & Modules Breakdown
================================================

This document explains all the methods used in the QR code scanning logic, categorized by their respective modules.

🔹 Module: cv2 (OpenCV)
-----------------------

OpenCV is used for **camera access, image processing, and QR code detection**.

### cv2.VideoCapture()

**Usage:**

```
cap = cv2.VideoCapture(0)
```


**Why used:** To access the system’s webcam for real-time video capture.

**Description:** Creates a video capture object that reads frames from the camera.0 refers to the default webcam.

### cap.read()

**Usage:**

```
ret, frame = cap.read()
```
**Why used:** To capture individual frames from the camera stream.

**Description:**

*   ret → Boolean value indicating success or failure
    
*   frame → Captured image frame (NumPy array)
    

### cv2.QRCodeDetector()

**Usage:**

```   
detector = cv2.QRCodeDetector()
```

**Why used:** To detect and decode QR codes without external libraries.

**Description:** Provides built-in QR code detection and decoding functionality in OpenCV.

### detector.detectAndDecode()

**Usage:**

```   
data, bbox, _ = detector.detectAndDecode(frame)
```

**Why used:** To locate and decode QR codes from a camera frame.

**Description:** Returns:

*   data → Decoded QR text
    
*   bbox → QR bounding box coordinates
    
*   \_ → Straightened QR image (not used here)
    

### cv2.imshow()

**Usage:**

```   
cv2.imshow("QR Code Scanner", frame)
```

**Why used:** To display live camera feed to the user.

**Description:** Opens a window showing real-time video capture.

### cv2.waitKey()

**Usage:**

```   
cv2.waitKey(1)
```

**Why used:** To listen for keyboard input and control frame refresh.

**Description:** Waits for a key press for the specified time in milliseconds.

### cv2.destroyAllWindows()

**Usage:**

```   
cv2.destroyAllWindows()
```

**Why used:** To properly close all OpenCV windows.

**Description:** Prevents hanging GUI windows and frees resources.

### cap.release()

**Usage:**

```   
cap.release()
```

**Why used:** To release the webcam resource after scanning.

**Description:** Stops camera capture and frees the device for other applications.

🔹 Python Built-in Functions
----------------------------

### print()

**Usage:**

```   
print("Scanning QR... Press 'q' to exit")
```

**Why used:** To display runtime instructions to the user.

**Description:** Outputs text to the console.

### ord()

**Usage:**

```   
ord('q')
```

**Why used:** To compare keyboard input with ASCII values.

**Description:** Returns the Unicode integer value of a character.

### str.strip()

**Usage:**

```   
data.strip()
```

**Why used:** To clean unwanted whitespace from QR data.

**Description:** Removes leading and trailing spaces from a string.

🔹 Control Flow & Language Constructs
-------------------------------------

### while True

**Why used:** To continuously scan frames until a QR code is detected.

**Description:** Creates an infinite loop for real-time scanning.

### if not ret

**Why used:** To ensure only valid frames are processed.

**Description:** Skips the loop iteration if camera frame capture fails.

### return

**Why used:** To immediately exit the function once QR data is detected.

**Description:** Returns the decoded QR value to the calling function.

📌 Summary
----------

ModulePurposecv2Camera access, QR detection, GUI displayBuilt-insInput handling, output, flow control
