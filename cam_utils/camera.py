import cv2
class Camera():

    def __init__(self, IP, username, password, applyModel, type, encode, name='Undefined', port=554):
        
        self.IP = IP
        self.port = port
        self.username = username
        self.password = password
        self.applyModel = applyModel
        self.type = type
        self.name = name
        self.encode = encode 
        # self.rtsp_url = f"rtsp://{self.username}:{self.password}@{self.IP}:{self.port}/stream"
        self.rtsp_url = f'rtsp://{self.username}:{self.password}@{self.IP}:{self.port}/media/video1'
        if encode == 'AVC':
            self.pipeline = f"rtspsrc location={self.rtsp_url} latency=0   ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! queue leaky=2 ! appsink"
        elif encode == 'HEVC':
            self.pipeline = f"rtspsrc location={self.rtsp_url} latency=0 ! rtph265depay ! h265parse ! avdec_h265 ! videoconvert ! queue leaky=2 ! appsink"
        self.isActive = self.check_pipeline()


    def check_pipeline(self):
        # Use OpenCV to open the GStreamer pipeline
        cap = cv2.VideoCapture(self.pipeline, cv2.CAP_GSTREAMER)
        
        # Check if the pipeline is opened successfully
        if not cap.isOpened():
            print("Pipeline failed to open")
            return False
        
        # Try to grab a frame from the stream
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab a frame")
            cap.release()
            return False
        
        # Pipeline is working; release the capture
        print("Pipeline works successfully!")
        cap.release()
        return True
