import cv2
from cam_utils.camera import Camera
from time import time, sleep
import urllib.parse
cv2.setLogLevel(4)

def main():
    # Create a Camera object
    cam1 = Camera('172.23.20.95', 'mdfproduct', 'mdfproduct_1', True, "wood", 'HEVC', 'test')

    # Define the GStreamer pipeline
    gst_pipeline = cam1.pipeline
    print(cam1.isActive)
    # Open the video capture using the GStreamer pipeline
    pw = urllib.parse.quote('mdfproduct@1')
    print(pw)
    t = f'rtsp://mdfproduct:{pw}@172.23.20.95:554/stream'
    print(cam1.pipeline)
    cap = cv2.VideoCapture(cam1.pipeline)

    # Check if the video capture is opened successfully
    if not cap.isOpened():
        print("Failed to open video capture")
        return

    # Process frames from the video stream
    while True:
        start = time()*1000
        # Read a frame from the video capture
        ret, frame = cap.read()
        print(time()*1000 - start)
        # Check if the frame is read successfully
        if not ret:
            print("Failed to read frame")
            continue
        # sleep(100 /1000.0)
        # Perform any desired operations on the frame
        # For example, you can display the frame
        cv2.imshow("Frame", frame)

        # Wait for a key press and check if 'q' is pressed to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture and close windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()