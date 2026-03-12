### NODE PURPOSE ###
"""
detecting humans with oak-d-lite camera
"""
### NODE PURPOSE ###


#!/usr/bin/env python3

import time
import argparse
import rclpy
from rclpy.node import Node
import depthai as dai

class HumanDetectionNode(Node):

    def __init__(self, nnPath):
        super().__init__('human_detection_node')

        # Create timer to call detect_persons every 0.5 seconds
        self.timer = self.create_timer(0.5, self.detect_persons)

        # Create pipeline
        self.pipeline = dai.Pipeline()

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
        self.camRgb.setFps(40)

        # Set the path for the MobileNet detection network
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

        # Connect to device and start pipeline
        self.device = dai.Device(self.pipeline)
        self.preview = self.device.getOutputQueue("preview", 4, False)
        self.tracklets = self.device.getOutputQueue("tracklets", 4, False)

        self.get_logger().info("HUMAN DETECTION NODE SUCCESSFULLY INITIATED")


    def detect_persons(self):
        startTime = time.monotonic()
        counter = 0
        fps = 0

        imgFrame = self.preview.get()
        track = self.tracklets.get()

        counter += 1
        current_time = time.monotonic()
        if (current_time - startTime) > 1:
            fps = counter / (current_time - startTime)
            counter = 0
            startTime = current_time

        # Get the tracking data
        trackletsData = track.tracklets
        
        # roi = region of interest
        for t in trackletsData:
            if t.label == 15:  # Only track persons (label 15)
                # Only log if the person is tracked
                if t.status == dai.Tracklet.TrackingStatus.TRACKED:  # Compare with the enum directly
                    roi = t.roi.denormalize(imgFrame.getWidth(), imgFrame.getHeight())
                    x1 = int(roi.topLeft().x)
                    y1 = int(roi.topLeft().y)

                    # Log detection data
                    self.get_logger().info(f" - Coordinates: ({x1}, {y1}) to ({int(roi.bottomRight().x)}, {int(roi.bottomRight().y)})")
                    self.get_logger().info(f" - Distance from top of frame to top of person: {y1} pixels")


def main(args=None):
    rclpy.init(args=args)

    # Default model path
    nnPathDefault = '/home/name/depthai-python/examples/models/mobilenet-ssd_openvino_2021.4_6shave.blob'
    parser = argparse.ArgumentParser()
    parser.add_argument('nnPath', nargs='?', help="Path to mobilenet detection network blob", default=nnPathDefault)
    args = parser.parse_args()

    node = HumanDetectionNode(nnPath=args.nnPath)

    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()