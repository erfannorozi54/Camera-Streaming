import cv2
from cam_utils.camera import Camera, CameraManager
from time import time, sleep
import urllib.parse
import asyncio
import logging

logging.basicConfig(
    level=logging.DEBUG,  # Log everything from DEBUG and higher levels
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Define the log format
    handlers=[logging.StreamHandler()]  # Output to the terminal (stdout)
)
logger = logging.getLogger(__name__)
# def main():
#     # Create a Camera object
#     cam1 = Camera('172.23.20.95', 'mdfproduct', 'mdfproduct@1', True, "wood", 'HEVC', 'test')

#     # Define the GStreamer pipeline
#     gst_pipeline = cam1.pipeline
#     print(cam1.isActive)
#     # Open the video capture using the GStreamer pipeline
#     pw = urllib.parse.quote('mdfproduct@1')
#     print(pw)
#     t = f'rtsp://mdfproduct:{pw}@172.23.20.95:554/stream'
#     print(cam1.pipeline)
#     cap = cv2.VideoCapture("rtspsrc location=rtsp://mdfproduct:mdfproduct%401@172.23.20.95:554/stream latency=20 ! rtph265depay ! h265parse ! avdec_h265 ! videoconvert ! queue leaky=2 ! appsink")

#     # Check if the video capture is opened successfully
#     if not cap.isOpened():
#         print("Failed to open video capture")
#         return

#     # Process frames from the video stream
#     while True:
#         start = time()*1000
#         # Read a frame from the video capture
#         ret, frame = cap.read()
#         print(time()*1000 - start)
#         # Check if the frame is read successfully
#         if not ret:
#             print("Failed to read frame")
#             continue
#         # Perform any desired operations on the frame
#         # For example, you can display the frame
#         cv2.imshow("Frame", frame)

#         # Wait for a key press and check if 'q' is pressed to quit
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     # Release the video capture and close windows
#     cap.release()
#     cv2.destroyAllWindows()

def callbk():
    print("Hello")
def main():
    manager = CameraManager()
    asyncio.run(manager.run())
    # asyncio.create_task(maneger.create_socket()) 
    # while True:
    #     print('Performing other tasks...')
    #     await asyncio.sleep(2)  # Simulate other work with async sleep


if __name__ == "__main__":
    main()