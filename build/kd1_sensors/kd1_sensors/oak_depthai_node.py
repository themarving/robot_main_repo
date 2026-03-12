### NODE PURPOSE ###
"""
combinbing all algorithms using the depthai package and the oak-d-lite depth camera:
    1. publishing pointcloud from depth image
    2. detecting humans with oak-d-lite camera and publishing frame offsets in order to center robot in front of person
    3. getting imu data froam oak-d-lite and publishing
"""
### NODE PURPOSE ###


#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Bool
from sensor_msgs.msg import PointCloud2, PointField

# using custom msg type
from custom_interfaces.msg import IMUData
from custom_interfaces.msg import DetectedPersonFrameOffset 

# DepthAI library for working with OAK cameras
import depthai as dai  
import numpy as np  
import struct

# for double ended queue (deque)
import collections  

# for human detection algorithm
import time


class OakDepthAINode(Node):
    def __init__(self):
        super().__init__("oak_depthai_node")
        
        # create the DepthAI pipeline
        self.pipeline = dai.Pipeline()
        

        ################################
        ### 1. POINTCLOUD GENERATION ###
        ################################

        # defining source nodes for the pipeline
        self.monoLeft = self.pipeline.create(dai.node.MonoCamera)
        self.monoRight = self.pipeline.create(dai.node.MonoCamera)
        self.stereo = self.pipeline.create(dai.node.StereoDepth)
        self.depthOut = self.pipeline.create(dai.node.XLinkOut)

        self.depthOut.setStreamName("depth")

        # configuring mono cameras
        self.monoLeft.setBoardSocket(dai.CameraBoardSocket.CAM_B)
        self.monoRight.setBoardSocket(dai.CameraBoardSocket.CAM_C)
        self.monoLeft.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
        self.monoRight.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)

        # configuring stereo depth node  
        self.stereo.setLeftRightCheck(True)
        self.stereo.setSubpixel(True)  # subpixel precision for better accuracy
        self.stereo.initialConfig.setConfidenceThreshold(200) # high confidence threshold for depth calculations

        # linking the nodes
        self.monoLeft.out.link(self.stereo.left)
        self.monoRight.out.link(self.stereo.right)
        self.stereo.depth.link(self.depthOut.input)

        # Publisher for PointCloud2
        self.pc2_pub = self.create_publisher(PointCloud2, 'depth_cam_pointcloud', 10)
        
        # Depth image size from stereo camera
        self.width = 640
        self.height = 400

        # Stereo camera parameters 
        self.fx = 365.0  # focal length x
        self.fy = 365.0  # focal length y
        self.cx = self.width / 2.0
        self.cy = self.height / 2.0
        self.baseline = 75.0  # mm (distance between cameras)
        
        
        ####################################
        ### 2. HUMAN DETECTION ALGORITHM ###
        ####################################
        
        # publisher for detected person frame offsets
        self.frame_offset_publisher = self.create_publisher(DetectedPersonFrameOffset, 'detected_person_frame_offset', 10)

        # Define sources and outputs
        self.camRgb = self.pipeline.create(dai.node.ColorCamera)
        self.detectionNetwork = self.pipeline.create(dai.node.MobileNetDetectionNetwork)
        self.objectTracker = self.pipeline.create(dai.node.ObjectTracker)

        self.xlinkOut = self.pipeline.create(dai.node.XLinkOut)
        self.trackerOut = self.pipeline.create(dai.node.XLinkOut)

        self.xlinkOut.setStreamName("preview")
        self.trackerOut.setStreamName("tracklets")

        # Properties
        self.camRgb.setPreviewSize(300, 300) 
        self.camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
        self.camRgb.setInterleaved(False)
        self.camRgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.BGR)
        self.camRgb.setFps(5) # SET FPS

        # Set the path for the MobileNet detection network
        nnPath = '/home/name/depthai-python/examples/models/mobilenet-ssd_openvino_2021.4_6shave.blob'

        self.detectionNetwork.setBlobPath(nnPath)
        self.detectionNetwork.setConfidenceThreshold(0.9)
        self.detectionNetwork.input.setBlocking(False)

        self.objectTracker.setDetectionLabelsToTrack([15])  # track only person
        self.objectTracker.setTrackerType(dai.TrackerType.ZERO_TERM_COLOR_HISTOGRAM)
        self.objectTracker.setTrackerIdAssignmentPolicy(dai.TrackerIdAssignmentPolicy.SMALLEST_ID)

        # Linking
        self.camRgb.preview.link(self.detectionNetwork.input)
        self.objectTracker.passthroughTrackerFrame.link(self.xlinkOut.input)
        self.detectionNetwork.passthrough.link(self.objectTracker.inputTrackerFrame)
        self.detectionNetwork.passthrough.link(self.objectTracker.inputDetectionFrame)
        self.detectionNetwork.out.link(self.objectTracker.inputDetections)
        self.objectTracker.out.link(self.trackerOut.input)
        
        
        ##############################
        ### 3. IMU DATA PROCESSING ###
        ##############################
        
        # publisher for IMU data
        self.imu_data_publisher = self.create_publisher(IMUData, 'imu_data', 10)

        # creating imu depthai node
        self.imu = self.pipeline.create(dai.node.IMU)

        # enabling raw IMU sensors (accelerometer and gyroscope)
        # Available rates in HZ
        # Accelerometer: 25Hz, 50Hz, 100Hz, 200Hz, 250Hz
        # Gyroscope: 25Hz, 50Hz, 100Hz, 200Hz, 250Hz
        self.imu.enableIMUSensor([dai.IMUSensor.ACCELEROMETER_RAW, dai.IMUSensor.GYROSCOPE_RAW], 25)  # SET TO 25Hz

        # configuring IMU batch parameters
        self.imu.setBatchReportThreshold(1)  # minimum number of packets per batch
        self.imu.setMaxBatchReports(10)  # maximum number of packets in a batch

        # creating XLinkOut node for imu data
        self.imuXlinkOut = self.pipeline.create(dai.node.XLinkOut)
        self.imuXlinkOut.setStreamName("imu")
        self.imu.out.link(self.imuXlinkOut.input)
        
        
        ######################
        ### SETUP COMPLETE ###
        ######################
        
        # shared DepthAI device
        self.oak_d_light_hardware_interface = None
        self.initialize_device()
        
        # calling all three functions
        self.create_timer(0.5, self.create_pointcloud)  # 2 Hz
        self.create_timer(1.5, self.detect_person) # 1 Hz
        self.create_timer(0.03, self.process_imu_data)  # 33 Hz

        self.get_logger().info("OAK DEPTH AI NODE SUCCESSFULLY INITIATED")
        
        
    #########################
    ### DEVICE CONNECTION ###
    #########################
    
    def initialize_device(self):
        try:
            self.oak_d_light_hardware_interface = dai.Device(self.pipeline)
            self.get_logger().info("OAK-D device initialized successfully.")
        except Exception as e:
            self.get_logger().error(f"Error initializing OAK-D device: {e}")
            self.oak_d_light_hardware_interface = None  # reset the interface
            self.reconnect_device()  # attempt reconnection

    def reconnect_device(self):
        if self.oak_d_light_hardware_interface is None:
            self.get_logger().warn("Attempting to reconnect to OAK-D device...")
            try:
                self.initialize_device()  # try re-initializing the device
            except Exception as e:
                self.get_logger().error(f"Reconnection failed: {e}")
                return
        else:
            self.get_logger().info("OAK-D device is connected.")
            

    ################################
    ### 1. POINTCLOUD GENERATION ###
    ################################
    
    def create_pointcloud(self):
        try:
            # Output queue from device
            q_depth = self.oak_d_light_hardware_interface.getOutputQueue(name="depth", maxSize=4, blocking=False)
            
            in_depth = q_depth.tryGet()
            
            if in_depth is None:
                return
            
            depth_frame = in_depth.getFrame()  # numpy array in mm

            # Convert depth image to point cloud XYZ
            points = []
            
            # DEFINES HOW MANY POINTS ARE CREATED FOR THE POINTCLOUD - massively corolates to processing speed of the node
            for v in range(0, self.height, 4):  # lower number = more points
                for u in range(0, self.width, 4):
                    z = depth_frame[v, u] / 1000.0  # mm to meters
                    
                    if z == 0:
                        continue
                    
                    x = (u - self.cx) * z / self.fx
                    y = (v - self.cy) * z / self.fy
                    
                    points.append([x, y, z])

            # Build PointCloud2 message
            msg = PointCloud2()
            msg.header.stamp = self.get_clock().now().to_msg()
            msg.header.frame_id = 'depth_camera_link' # CONNECTING TO ROBOT DESCRIPTION
            msg.height = 1
            msg.width = len(points)
            msg.is_dense = False
            msg.is_bigendian = False
            msg.point_step = 12  # 3 float32
            msg.row_step = msg.point_step * msg.width
            msg.fields = [
                PointField(name='x', offset=0, datatype=PointField.FLOAT32, count=1),
                PointField(name='y', offset=4, datatype=PointField.FLOAT32, count=1),
                PointField(name='z', offset=8, datatype=PointField.FLOAT32, count=1),
            ]

            # pack points into binary blob
            buffer = []
            
            for p in points:
                buffer.append(struct.pack('fff', *p))
                
            msg.data = b"".join(buffer)

            self.pc2_pub.publish(msg)
                    
        except Exception as e:
            self.get_logger().error(f"Error in create_pointcloud: {e}")
            self.oak_d_light_hardware_interface = None  # reset the interface
            self.reconnect_device()  # attempt reconnection
            
            
    ####################################
    ### 2. HUMAN DETECTION ALGORITHM ###
    ####################################
    
    # def detect_person(self):
    #     try: 
    #         preview = self.oak_d_light_hardware_interface.getOutputQueue("preview", 4, False)
    #         tracklets = self.oak_d_light_hardware_interface.getOutputQueue("tracklets", 4, False)
            
    #         startTime = time.monotonic()
    #         counter = 0

    #         imgFrame = preview.get()
    #         track = tracklets.get()

    #         counter += 1
    #         current_time = time.monotonic()
    #         if (current_time - startTime) > 1:
    #             counter = 0
    #             startTime = current_time

    #         # Get the tracking data
    #         trackletsData = track.tracklets
            
    #         # roi = region of interest
    #         for t in trackletsData:
    #             if t.label == 15:  # Only track persons (label 15)
    #                 # Only log if the person is tracked
    #                 if t.status == dai.Tracklet.TrackingStatus.TRACKED:  # Compare with the enum directly
    #                     roi = t.roi.denormalize(imgFrame.getWidth(), imgFrame.getHeight())
                        
    #                     # Extract the coordinates of the top-left and bottom-right corners of the bounding box (ROI)
    #                     x1 = int(roi.topLeft().x)  # x-coordinate of the top-left corner of the bounding box
    #                     y1 = int(roi.topLeft().y)  # y-coordinate of the top-left corner of the bounding box
    #                     x2 = int(roi.bottomRight().x)  # x-coordinate of the bottom-right corner of the bounding box
    #                     y2 = int(roi.bottomRight().y)  # y-coordinate of the bottom-right corner of the bounding box

    #                     # Calculate the center point of the bounding box
    #                     center_x = (x1 + x2) // 2  # Horizontal center of the bounding box (average of x1 and x2)
    #                     center_y = (y1 + y2) // 2  # Vertical center of the bounding box (average of y1 and y2)

    #                     # Get the center point of the frame (image)
    #                     frame_center_x = imgFrame.getWidth() // 2  # Horizontal center of the frame (half of the image width)
    #                     frame_center_y = imgFrame.getHeight() // 2  # Vertical center of the frame (half of the image height)

    #                     # Calculate the x offset: positive if person is to the left of the frame center, negative if to the right
    #                     x_offset = center_x - frame_center_x  # Difference between the person's horizontal center and the frame's center

    #                     # Calculate the y offset: positive if person is below the frame center, negative if above
    #                     y_offset = center_y - frame_center_y  # Difference between the person's vertical center and the frame's center
                        
    #                     ### FRAME OFFSET DATA MEANING ###
    #                     # x > 0: person right from center (robot pov)
    #                     # x < 0: person left from center (robot pov)
    #                     # x good range: 30 to -30
                        
    #                     # y > 0: person further away from robot than center
    #                     # y < 0: person closer to robot than center
    #                     # y good range everything 0 to 10
                        
    #                     # Create and publish the custom message
    #                     msg = DetectedPersonFrameOffset()
                        
    #                     msg.x_offset = float(x_offset)
    #                     msg.y_offset = float(y_offset)
                        
    #                     self.frame_offset_publisher.publish(msg)
                        
    #     except Exception as e:
    #         self.get_logger().error(f"Error in detect_person: {e}")
    #         self.oak_d_light_hardware_interface = None  # reset the interface
    #         self.reconnect_device()  # attempt reconnection

    def detect_person(self):
        try:
            # --- Get output queues ---
            preview = self.oak_d_light_hardware_interface.getOutputQueue("preview", 4, False)
            tracklets = self.oak_d_light_hardware_interface.getOutputQueue("tracklets", 4, False)
            depth_q = self.oak_d_light_hardware_interface.getOutputQueue("depth", 4, False)

            imgFrame = preview.get()
            track = tracklets.get()
            depthFrame = depth_q.tryGet()
            if depthFrame is None:
                return
            depth_frame = depthFrame.getFrame()  # depth in mm

            trackletsData = track.tracklets

            for t in trackletsData:
                if t.label != 15:  # only persons
                    continue
                if t.status != dai.Tracklet.TrackingStatus.TRACKED:
                    continue

                ### STEP 1: DETECT HUMAN ###
                roi = t.roi.denormalize(imgFrame.getWidth(), imgFrame.getHeight())
                x1, y1 = int(roi.topLeft().x), int(roi.topLeft().y)
                x2, y2 = int(roi.bottomRight().x), int(roi.bottomRight().y)
                center_x = (x1 + x2) // 2
                center_y = (y1 + y2) // 2

                ### STEP 2: GET DEPTH AT HUMAN LOCATION ###
                depth_patch = depth_frame[y1:y2, x1:x2]
                depth_patch = depth_patch[depth_patch > 0]  # remove invalid pixels
                if len(depth_patch) == 0:
                    continue
                Z_m = np.mean(depth_patch) / 1000.0  # convert mm -> meters

                ### STEP 3: COMPUTE REAL-WORLD X/Y COORDINATES ###
                # Using camera intrinsics
                X = Z_m  # forward distance from camera
                Y = (center_x - self.cx) * Z_m / self.fx  # left/right in meters, positive = right

                # --- Publish offsets ---
                msg = DetectedPersonFrameOffset()
                msg.x_offset = float(X)   # forward
                msg.y_offset = float(Y)   # left/right
                self.frame_offset_publisher.publish(msg)

        except Exception as e:
            self.get_logger().error(f"Error in detect_person: {e}")
            self.oak_d_light_hardware_interface = None
            self.reconnect_device()


                    
    ##############################
    ### 3. IMU DATA PROCESSING ###
    ##############################
    
    def process_imu_data(self):
        try:
            imuQueue = self.oak_d_light_hardware_interface.getOutputQueue(name="imu", maxSize=50, blocking=False)
            imuData = imuQueue.tryGet()
            
            if imuData:
                for packet in imuData.packets:
                    # extracting raw accelerometer and gyroscope data
                    accel = packet.acceleroMeter
                    gyro = packet.gyroscope
                    
                    msg = IMUData()
                    
                    # acceleration around axes in m/s^2
                    msg.accelerometer_x = accel.x
                    msg.accelerometer_y = accel.y
                    msg.accelerometer_z = accel.z
                    
                    # rotational speed around axes in rad/s
                    msg.gyroscope_x = gyro.x
                    msg.gyroscope_y = gyro.y
                    msg.gyroscope_z = gyro.z
                    
                    self.imu_data_publisher.publish(msg)
                    
        except Exception as e:
            self.get_logger().error(f"Error in process_imu_data: {e}")
            self.oak_d_light_hardware_interface = None  # reset the interface
            self.reconnect_device()  # attempt reconnection


def main(args=None):
    rclpy.init(args=args)
    
    node = OakDepthAINode()
    
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()