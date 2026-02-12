import cv2

def find_camera():
    for index in range(5):  # try 0–4
        cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
        if cap.isOpened():
            print(f"Camera found at index {index}")
            return cap
        cap.release()
    return None

cap = find_camera()

if cap is None:
    print("Camera not detected")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    cv2.imshow("Webcam", frame)

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
