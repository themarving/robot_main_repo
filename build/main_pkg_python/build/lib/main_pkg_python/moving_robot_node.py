### NODE PURPOSE ###
"""
moving robot head and driving around
"""
### NODE PURPOSE ###


#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from std_msgs.msg import String, Float32MultiArray

# custom services and messages
from custom_interfaces.msg import IMUData

import time

# ros2 topic pub /move_robot_command std_msgs/msg/String "data: forwards_fast" --once
# ros2 topic pub /move_robot_command std_msgs/msg/String "data: head_up" --once

class MovingRobotNode(Node): 
    def __init__(self):
        super().__init__("moving_robot_node")
        
        self.current_move_command = ""
        
        # subscriber to receive movement commands
        self.subscription = self.create_subscription(
            String,
            'move_robot_command',
            self.process_command,
            10
        )
        
        # motor driver commands publisher
        self.motor_driver_commands_publisher = self.create_publisher(
            Float32MultiArray, 
            'motor_driver_commands', 
            10
        )
        
        # possible move commands
        self.move_commands = [
            "forwards_fast", 
            "forwards_slow", 
            "backwards_fast", 
            "backwards_slow",
            "turn_left",
            "turn_right",
            "head_straight",
            "head_up",
            "head_down",
            "init_move"
        ]
        
        # map commands to handler methods
        self.command_handlers = {
            "forwards_fast": self.move_forwards_fast,
            "forwards_slow": self.move_forwards_slow,
            "backwards_fast": self.move_backwards_fast,
            "backwards_slow": self.move_backwards_slow,
            "turn_left": self.turn_left,
            "turn_right": self.turn_right,
            "head_straight": self.head_straight,
            "head_up": self.head_up,
            "head_down": self.head_down,
            "init_move": self.init_move
        }
        
        self.execute_command_timer = self.create_timer(0.1, self.execute_command)
        
        self.get_logger().info("MOVING ROBOT NODE SUCCESSFULLY INITIATED")
        
        
    def process_command(self, msg):   
        if msg.data in self.move_commands:
            self.current_move_command = msg.data
        else:
            self.get_logger().error("RECEIVED NON-EXISTENT MOVE COMMAND!") 

    
    def execute_command(self):
        if self.current_move_command in self.command_handlers:
            self.command_handlers[self.current_move_command]()    
        
        
    def move_forwards_fast(self):
        self.get_logger().info("Moving forwards fast!")

    def move_forwards_slow(self):
        self.get_logger().info("Moving forwards slow!")

    def move_backwards_fast(self):
        self.get_logger().info("Moving backwards fast!")

    def move_backwards_slow(self):
        self.get_logger().info("Moving backwards slow!")

    def turn_left(self):
        self.get_logger().info("Turning left!")
                
    def turn_right(self):
        self.get_logger().info("Turning right!")

    def head_straight(self):
        self.current_move_command = ""
        
        self.get_logger().info("Head straight!")

    def head_up(self):
        self.current_move_command = ""
        
        self.get_logger().info("Head up!")

    def head_down(self):
        self.current_move_command = ""
        
        self.get_logger().info("Head down!")
    
    def init_move(self):
        command1 = Float32MultiArray()
        command1.data = [100.0, 100.0, 90.0, 90.0]
        self.motor_driver_commands_publisher.publish(command1)
        time.sleep(0.5)

        command2 = Float32MultiArray()
        command2.data = [0.0, 0.0, 90.0, 90.0]
        self.motor_driver_commands_publisher.publish(command2)
        time.sleep(0.5)
                
        command3 = Float32MultiArray()
        command3.data = [-100.0, -100.0, 90.0, 90.0]
        self.motor_driver_commands_publisher.publish(command3)
        time.sleep(0.5)

        command4 = Float32MultiArray()
        command4.data = [0.0, 0.0, 90.0, 90.0]
        self.motor_driver_commands_publisher.publish(command4)
        time.sleep(0.5)
        
        self.current_move_command = ""
        

def main(args=None):
    rclpy.init(args=args)
    node = MovingRobotNode()
    
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()