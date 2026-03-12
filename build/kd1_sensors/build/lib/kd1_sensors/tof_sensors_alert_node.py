### NODE PURPOSE ###
"""
subscribing to tof data and evaluating for publishing tof sensors alert
"""
### NODE PURPOSE ###


#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool, Int64MultiArray


class TOFSensorsAlertNode(Node):
    def __init__(self):
        super().__init__("tof_sensors_alert_node")
        
        # tof data subscriber
        self.tof_data_subscriber = self.create_subscription(
            Int64MultiArray,
            'tof_distances_mm',
            self.checkForObstacle,
            10
        )
        
        # tof alert publisher
        self.tof_alert_publisher = self.create_publisher(
            Bool, 
            'tof_sensors_alert', 
            10
        )
        
        # default to is_obstructed
        self.is_obstructed = True

        self.get_logger().info("TOF SENSORS ALERT NODE SUCCESSFULLY INITIATED")
        
    
    def checkForObstacle(self, msg):
        # validate message length
        if len(msg.data) != 2:
            self.get_logger().warn("TOF data length != 2!")
            return

        # Extract current encoder ticks for left and right wheels
        left_tof = msg.data[0]
        right_tof = msg.data[1]
        
        # check for obstruction
        if left_tof < 400 or right_tof < 400:
            self.is_obstructed = True
        else: 
            self.is_obstructed = False
        
        alert_message = Bool()
        alert_message.data = True if self.is_obstructed else False
        self.tof_alert_publisher.publish(alert_message)


def main(args=None):
    rclpy.init(args=args)
    node = TOFSensorsAlertNode()

    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()