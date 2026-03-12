### NODE PURPOSE ###
"""
executing emergency stops based off of sensor data
"""
### NODE PURPOSE ###

#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from std_msgs.msg import Bool
from sensor_msgs.msg import Range


class EmergencyStopNode(Node):
    def __init__(self):
        super().__init__('emergency_stop_node')
        
        # tof values
        # min_range = 0.03 meters
        # max_range = 1.0 meters
        
        self.current_tof_front_left = 1.0
        self.current_tof_front_right = 1.0
        self.current_tof_back_left = 1.0
        self.current_tof_back_right = 1.0
        
        self.emergency_threshold = 0.25
        self.tof_blocked_counter = 0
        self.block_threshold = 2
        
        self.obstacle_detected = False
        
        # SUBSRIBERS FOR EACH TOF SENSOR
        self.tof_front_left_subscriber = self.create_subscription(
            Range,
            'tof_front_left',
            self.update_tof_front_left,
            10
        )
        
        self.tof_front_right_subscriber = self.create_subscription(
            Range,
            'tof_front_right',
            self.update_tof_front_right,
            10
        )
        
        self.tof_back_left_subscriber = self.create_subscription(
            Range,
            'tof_back_left',
            self.update_tof_back_left,
            10
        )

        self.tof_back_right_subscriber = self.create_subscription(
            Range,
            'tof_back_right',
            self.update_tof_back_right,
            10
        )
        
        # EMERGENCY STOP PUBLISHER
        self.emergency_stop_publisher = self.create_publisher(
            Bool,
            'execute_emergency_stop',
            10
        )
        
        self.check_for_obstacle_timer = self.create_timer(0.1, self.check_for_obstacle)
        
        self.get_logger().info("EMERGENCY STOP NODE SUCCESSFULLY INITIATED")
        
    
    def update_tof_front_left(self, msg):
        self.current_tof_front_left = msg.range

    def update_tof_front_right(self, msg):
        self.current_tof_front_right = msg.range
        
    def update_tof_back_left(self, msg):
        self.current_tof_back_left = msg.range
        
    def update_tof_back_right(self, msg):
        self.current_tof_back_right = msg.range
        
    
    # sending out emergency stop message
    def check_for_obstacle(self):
        if any(value < self.emergency_threshold for value in [
            self.current_tof_front_left,
            self.current_tof_front_right,
            self.current_tof_back_left,
            self.current_tof_back_right
        ]):
            if not self.obstacle_detected and self.tof_blocked_counter > self.block_threshold:
                self.obstacle_detected = True
                msg = Bool(data=True)
                self.emergency_stop_publisher.publish(msg)
                
                self.get_logger().warn("EMERGENCY STOP INITIATED!")
            elif not self.obstacle_detected:
                self.tof_blocked_counter += 1
        else:
            if self.obstacle_detected:
                self.obstacle_detected = False
                msg = Bool(data=False)
                self.emergency_stop_publisher.publish(msg)
                
                self.get_logger().info("OBSTRUCTION CLEARED!")
                
            self.tof_blocked_counter = 0
            

def main(args=None):
    rclpy.init(args=args)                    
    node = EmergencyStopNode()             
    try:
        rclpy.spin(node)                     
    finally:
        rclpy.shutdown()                   

if __name__ == '__main__':
    main()