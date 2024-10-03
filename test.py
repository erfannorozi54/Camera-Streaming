import cv2
from cam_utils.camera import Camera
from time import time, sleep

def main():
    # Create a Camera object
    cam1 = Camera('192.168.23.174', '533', 'express', '_rianExpress123456', True, "wood", 'test')

    # Define the GStreamer pipeline
    gst_pipeline = f"rtspsrc location={cam1.rtsp_url} latency=0 ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! appsink"
    gst_pipeline = f"rtspsrc location={cam1.rtsp_url} latency=0 ! rtph265depay ! h265parse ! avdec_h265 ! videoconvert ! queue leaky=2 ! appsink"


    # Open the video capture using the GStreamer pipeline
    cap = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)

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
            break

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