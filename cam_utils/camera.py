import cv2
import urllib.parse
from time import sleep
import socket
import asyncio
import os
from time import sleep
import requests
import logging
import struct

logger = logging.getLogger(__name__)



class CameraManager():

    def __init__(self) -> None:
        self.SOCKET_FILE = '/tmp/unix_socket'
        self.EOS_FLAG = b'__EOS__'  # Flag to indicate end of stream
        self.cameras = []
        self.isConncted = False
        self.camera_tasks = {}

    async def get_or_udate_cameras(self,test=False):
        if test:
            self.cameras = [Camera('172.23.20.95', 'mdfproduct', 'mdfproduct_1', True, "wood", 'HEVC', 'test'),Camera('172.23.20.93', 'mdfproduct', 'mdfproduct_1', True, "wood", 'HEVC', 'test2')]
            return 1
        else:
            api_url = "https://api.example.com/cameras"  # Replace with your actual API endpoint
            loop = asyncio.get_event_loop()
            try:
                # Use asyncio's run_in_executor to make the synchronous requests call non-blocking
                response = await loop.run_in_executor(None, requests.get, api_url)
                
                # Check if the response was successful
                if response.status_code == 200:
                    data = response.json()
                    new_cameras = data.get('cameras', [])
                    # Update self.cameras if new cameras exist
                    for cam in new_cameras:
                        if cam not in self.cameras:
                            self.cameras.append(cam)
                            print(f"New camera added: {cam}")
                else:
                    print(f"Error fetching cameras: {response.status_code}")
            except requests.RequestException as e:
                print(f"An HTTP error occurred: {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

    # async def create_socket(self):

    #     if os.path.exists(self.SOCKET_FILE):
    #         os.remove(self.SOCKET_FILE)
    #     self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    #     self.sock.bind(self.SOCKET_FILE)
    #     self.sock.listen(1)
    #     await self.accept_connections(self.sock)
    #     # await self.accept_connections(self.sock)

    # def _handle_connection(self,connection):
    #     # Callback function to handle connection
    #     print('Connected!')
    #     self.isConncted = True

    # async def accept_connections(self,sock):
    #     connection, _ = await asyncio.get_event_loop().run_in_executor(None, sock.accept)
    #     self._handle_connection(connection)
    async def create_socket(self):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.settimeout(1)
        self.sock.connect(self.SOCKET_FILE)
        

    
    async def run(self):
        # Start background tasks for socket creation and camera updating
        asyncio.create_task(self.create_socket())
        asyncio.create_task(self.get_or_udate_cameras(test=True))
        
        while True:
            if not self.isConncted:
                asyncio.create_task(self.create_socket())
            asyncio.create_task(self.get_or_udate_cameras(test=True))
            await asyncio.sleep(10)
            # Check if there are any cameras in the list
            if len(self.cameras) != 0:
                # Loop over all cameras and check if they already have tasks
                for camera in self.cameras:
                    if camera.IP not in self.camera_tasks.keys() or self.camera_tasks[camera.IP].done():
                        logger.info(f"in if and {camera.IP not in self.camera_tasks.keys()}")
                        # Create a new task for the camera's `get_stream` method if none exists or the previous one is done
                        print(f"Creating stream task for camera {camera.IP}")
                        try:
                            task = asyncio.create_task(camera.get_stream(self.isConncted,socket=self.sock))
                        except Exception as e:
                            logger.error(f'task for camera {camera.name} can not created!')
                            logger.error(e)
                        self.camera_tasks[camera.IP] = task
                    else:
                        print(f"Camera {camera} is already streaming.")
            
            # Sleep a bit before checking again to avoid unnecessary CPU usage
            await asyncio.sleep(10)



class Camera():

    def __init__(self, IP, username, password, applyModel, type, encode, name='Undefined', port=554,useGstreamer=False):
        
        self.IP = IP
        self.port = port
        self.username = username
        self.password = urllib.parse.quote(password)
        self.applyModel = applyModel
        self.type = type
        self.name = name
        self.encode = encode 
        self.bad_frames = 0
        # self.rtsp_url = f"rtsp://{self.username}:{self.password}@{self.IP}:{self.port}/stream"
        # self.rtsp_url = f'rtsp://{self.username}:{self.password}@{self.IP}:{self.port}/media/video1'
        self.rtsp_url = f'rtsp://{self.username}:{self.password}@{self.IP}:{self.port}/stream'
        if useGstreamer:
            if encode == 'AVC':
                self.pipeline = f"rtspsrc location={self.rtsp_url} latency=0 ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! queue leaky=2 ! appsink"
            elif encode == 'HEVC':
                # self.pipeline = f"rtspsrc location={self.rtsp_url} latency=300 ! rtph265depay ! h265parse ! avdec_h265 ! videoconvert ! queue leaky=2 ! appsink"
                # self.pipeline = f"rtspsrc location={self.rtsp_url} latency=0 ! rtph265depay ! h265parse ! avdec_h265 ! videoconvert ! queue ! appsink"
                self.pipeline = f"rtspsrc location={self.rtsp_url} latency=1000 ! rtph265depay ! h265parse ! avdec_h265 ! videoconvert ! appsink"
        else:
            self.pipeline = self.rtsp_url


        self.isActive = self.check_pipeline()
        try:
            logger.info(f'isActive att is {self.isActive}')
        except:
            logger.info('isActive att is logging error')
        if self.isActive:
            self.stream = cv2.VideoCapture(self.pipeline)


    def check_pipeline(self):
        # Use OpenCV to open the GStreamer pipeline
        print(self.pipeline)
        cap = cv2.VideoCapture(self.pipeline)
        print("---------------")
        print(cap.isOpened())
        
        # Check if the pipeline is opened successfully
        if not cap.isOpened():
            print("Pipeline failed to open")
            return False
        
        print("Pipeline works successfully!")
        cap.release()
        return True
    
    async def get_stream(self,isSocketConnected,socket):
        logger.info(isSocketConnected)
        loop = asyncio.get_event_loop()
        frame_counter = 0
        skip_factor = 30
        while True:
            print(isSocketConnected)
            logger.info(isSocketConnected)

            # Run the blocking stream.read() in an executor to avoid blocking the event loop
            ret, frame = await loop.run_in_executor(None, self.stream.read)
            if not ret:
                print("Failed to get frame, exiting stream.")
                self.bad_frames += 1
                if self.bad_frames >= 10:
                    raise RuntimeError("Too many bad frames encountered (10). Stream is invalid.")
                else:
                    pass

            frame_counter += 1
            if frame_counter % skip_factor != 0:
                # Display the frame
                continue


            
            # Process the frame (e.g., display, save, or stream it)
            logger.info(f'Got a frame from the camera {self.name} and ret is {ret}')
            if isSocketConnected:
                socket.sendall(frame)
                response = await loop.run_in_executor(None, socket.recv,4)
                response_int = struct.unpack('!I', response)[0]

                # send request to API



