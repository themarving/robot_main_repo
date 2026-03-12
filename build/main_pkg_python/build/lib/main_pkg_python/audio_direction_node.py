### NODE PURPOSE ###
"""
getting current audio direction from mic array and publishing direction
"""
### NODE PURPOSE ###


#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int16

# adding file path for tuning.py
import sys
sys.path.append('/home/name/kd1_ws/src/main_pkg_python')

from tuning import Tuning
import usb.core
import usb.util

class AudioDirectionNode(Node): 
    def __init__(self):
        super().__init__("audio_direction_node")
        
        dev = usb.core.find(idVendor=0x2886, idProduct=0x0018)
        
        self.Mic_tuning = Tuning(dev)
        
        # creating publisher for audio direction
        self.audio_direction_publisher = self.create_publisher(Int16, 'audio_direction', 10)
        
        self.timer = self.create_timer(0.1, self.detect_audio_direction)
        
        self.get_logger().info("AUDIO DIRECTION NODE SUCCESSFULLY INITIATED")
        
    
    def detect_audio_direction(self):
        msg = Int16()
        msg.data = self.Mic_tuning.direction
        self.audio_direction_publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = AudioDirectionNode()
    
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()