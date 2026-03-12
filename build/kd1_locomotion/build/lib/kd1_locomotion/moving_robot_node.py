### NODE PURPOSE ###
"""
moving robot head and driving around
"""
### NODE PURPOSE ###


#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from std_msgs.msg import Float32MultiArray

# custom services and messages
from custom_interfaces.msg import IMUData, MoveRobotCommand

import time
import math

# ros2 topic pub /move_robot_command custom_interfaces/msg/MoveRobotCommand "{command: 'turn_left', goal_angle: 90.0}" --once
# ros2 topic pub /move_robot_command custom_interfaces/msg/MoveRobotCommand "{command: 'turn_right', goal_angle: 90.0}" --once
# ros2 topic pub /move_robot_command custom_interfaces/msg/MoveRobotCommand "{command: 'stop', goal_angle: 0.0}" --once

class MovingRobotNode(Node): 
    def __init__(self):
        super().__init__("moving_robot_node")
        
        self.current_move_command = ""
        
        self.standard_servo_angle_left = 93.0
        self.standard_servo_angle_right = 87.0
        self.current_servo_angle_left = self.standard_servo_angle_left
        self.current_servo_angle_right = self.standard_servo_angle_right
        
        # subscriber to receive movement commands
        self.subscription = self.create_subscription(
            MoveRobotCommand,
            'move_robot_command',
            self.process_command,
            10
        )
        
        # imu data
        self.imu_data_subscriber = self.create_subscription(
            IMUData,
            'imu_data',
            self.process_imu_data,
            10
        )
        
        self.turning_left = False
        self.turning_right = False
        self.yaw_accumulated = 0.0  # in radians
        self.last_imu_time = self.get_clock().now()
        
        self.current_requested_turn_angle = 0.0

        # motor driver commands publisher
        self.motor_driver_commands_publisher = self.create_publisher(
            Float32MultiArray, 
            'motor_driver_commands', 
            10
        )
        
        # possible move commands
        self.move_commands = [
            "stop",
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
            "stop": self.stop_robot,
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
        if msg.command in self.move_commands:
            self.current_move_command = msg.command
            
            # setting requested_turn_angle - 5 to compensate for overturning
            if msg.goal_angle > 5:
                self.current_requested_turn_angle = msg.goal_angle - 5
        else:
            self.get_logger().error("RECEIVED NON-EXISTENT MOVE COMMAND!") 
            
    
    def execute_command(self):
        if self.current_move_command in self.command_handlers:
            self.command_handlers[self.current_move_command]()      
            

    def process_imu_data(self, msg):
        if self.turning_right and self.turning_left:
            self.turning_right = False
            self.turning_left = False
        
        # LEFT TURN
        if self.turning_left:
            # Get the current time using the ROS clock
            now = self.get_clock().now()

            # Compute the time difference (dt) in seconds between now and the last received IMU message
            dt = (now - self.last_imu_time).nanoseconds * 1e-9  # Convert nanoseconds to seconds

            # Update the last IMU timestamp for the next callback
            self.last_imu_time = now

            # Extract the angular velocity around the y-axis from the IMU message (in radians per second)
            angular_velocity_rad = msg.gyroscope_y  # rad/s

            # Compute the change in yaw (angle) over this time period
            delta_yaw = angular_velocity_rad * dt   # rad

            # Accumulate the total yaw rotation
            self.yaw_accumulated += delta_yaw

            # GOAL REACHED
            if abs(self.yaw_accumulated) >= math.radians(self.current_requested_turn_angle):
                self.stop_robot()
                self.current_requested_turn_angle = 0.0
                self.turning_left = False
                   
        # RIGHT TURN 
        if self.turning_right:
            now = self.get_clock().now()
            dt = (now - self.last_imu_time).nanoseconds * 1e-9
            self.last_imu_time = now

            angular_velocity_rad = msg.gyroscope_y

            delta_yaw = angular_velocity_rad * dt

            # subtracting, because right turns give negativ gyro values
            self.yaw_accumulated -= delta_yaw

            # GOAL REACHED
            if abs(self.yaw_accumulated) >= math.radians(self.current_requested_turn_angle):
                self.stop_robot()
                self.current_requested_turn_angle = 0.0
                self.turning_right = False
        
        
    def stop_robot(self):
        command = Float32MultiArray()
        command.data = [0.0, 0.0, self.current_servo_angle_left, self.current_servo_angle_right]
        self.motor_driver_commands_publisher.publish(command)
        
        self.current_move_command = ""
        
        
    def move_forwards_fast(self):
        self.set_standard_head_angle()
        
        command = Float32MultiArray()
        command.data = [255.0, 255.0, self.current_servo_angle_left, self.current_servo_angle_right]
        self.motor_driver_commands_publisher.publish(command)


    def move_forwards_slow(self):
        self.set_standard_head_angle()
        
        command = Float32MultiArray()
        command.data = [100.0, 100.0, self.current_servo_angle_left, self.current_servo_angle_right]
        self.motor_driver_commands_publisher.publish(command)


    def move_backwards_fast(self):
        self.set_standard_head_angle()
        
        command = Float32MultiArray()
        command.data = [-255.0, -255.0, self.current_servo_angle_left, self.current_servo_angle_right]
        self.motor_driver_commands_publisher.publish(command)


    def move_backwards_slow(self):
        self.set_standard_head_angle()
        
        command = Float32MultiArray()
        command.data = [-100.0, -100.0, self.current_servo_angle_left, self.current_servo_angle_right]
        self.motor_driver_commands_publisher.publish(command)


    def turn_left(self):
        self.set_standard_head_angle()
        
        self.yaw_accumulated = 0.0
        self.last_imu_time = self.get_clock().now()
        self.turning_left = True
        self.turning_right= False

        command = Float32MultiArray()
        command.data = [-100.0, 100.0, self.current_servo_angle_left, self.current_servo_angle_right]
        self.motor_driver_commands_publisher.publish(command)
        
        self.current_move_command = ""   
           
                
    def turn_right(self):
        self.set_standard_head_angle()
        
        self.yaw_accumulated = 0.0
        self.last_imu_time = self.get_clock().now()
        self.turning_left = False
        self.turning_right = True

        command = Float32MultiArray()
        command.data = [100.0, -100.0, self.current_servo_angle_left, self.current_servo_angle_right]
        self.motor_driver_commands_publisher.publish(command)
        
        self.current_move_command = ""


    def head_straight(self):
        self.current_move_command = ""
        
        self.current_servo_angle_left = self.standard_servo_angle_left
        self.current_servo_angle_right = self.standard_servo_angle_right
        
        command = Float32MultiArray()
        command.data = [0.0, 0.0, self.current_servo_angle_left, self.current_servo_angle_right]
        self.motor_driver_commands_publisher.publish(command)


    def head_up(self):
        self.current_move_command = ""
        
        self.current_servo_angle_left = self.standard_servo_angle_left - 20
        self.current_servo_angle_right = self.standard_servo_angle_right + 20
        
        command = Float32MultiArray()
        command.data = [0.0, 0.0, self.current_servo_angle_left, self.current_servo_angle_right]
        self.motor_driver_commands_publisher.publish(command)


    def head_down(self):
        self.current_move_command = ""
        
        self.current_servo_angle_left = self.standard_servo_angle_left + 20
        self.current_servo_angle_right = self.standard_servo_angle_right - 20
        
        command = Float32MultiArray()
        command.data = [0.0, 0.0, self.current_servo_angle_left, self.current_servo_angle_right]
        self.motor_driver_commands_publisher.publish(command)
    
    
    def init_move(self):
        command = Float32MultiArray()
        command.data = [0.0, 0.0, self.standard_servo_angle_left + 20, self.standard_servo_angle_right - 20]
        self.motor_driver_commands_publisher.publish(command)
        time.sleep(2.0)
                
        command2 = Float32MultiArray()
        command2.data = [0.0, 0.0, self.standard_servo_angle_left, self.standard_servo_angle_right]
        self.motor_driver_commands_publisher.publish(command2)
        
        self.current_servo_angle_left = self.standard_servo_angle_left
        self.current_servo_angle_right = self.standard_servo_angle_right
        
        self.current_move_command = ""
        
        
    # standard head angle while driving for odometry with imu
    def set_standard_head_angle(self):
        self.current_servo_angle_left = self.standard_servo_angle_left
        self.current_servo_angle_right = self.standard_servo_angle_right
        

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