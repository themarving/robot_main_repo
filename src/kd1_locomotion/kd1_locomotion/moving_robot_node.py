### NODE PURPOSE ###
"""
moving robot head and driving around, driving forwards and backwards speeds are sent constantly to 
motor_driver_comms_node because that is how the wheel drift is removed
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
import random


# ros2 topic pub /move_robot_command custom_interfaces/msg/MoveRobotCommand "{command: 'head_straight', goal_angle: 90.0}" --once
# ros2 topic pub /move_robot_command custom_interfaces/msg/MoveRobotCommand "{command: 'stop', goal_angle: 30.0}" --once
# ros2 topic pub /move_robot_command custom_interfaces/msg/MoveRobotCommand "{command: 'forwards_slow', goal_angle: 0.0}" --once

class MovingRobotNode(Node): 
    def __init__(self):
        super().__init__("moving_robot_node")
        
        self.current_move_command = ""
        
        self.current_left_speed = 0.0
        self.current_right_speed = 0.0
        
        self.standard_servo_angle = 90.0
        self.current_servo_angle = self.standard_servo_angle
        
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
        
        self.max_speed = 160.0
        self.slow_speed = 100.0
        self.turning_speed = 140.0
        self.turning_correction_angle = 15
        
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
            "head_left",
            "head_half_left",
            "head_right",
            "head_half_right",
            "init_move",
            "shake_head"
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
            "head_left": self.head_left,
            "head_half_left": self.head_half_left,
            "head_right": self.head_right,
            "head_half_right": self.head_half_right,
            "init_move": self.init_move,
            "shake_head": self.shake_head
        }
        
        self.execute_command_timer = self.create_timer(0.1, self.execute_command)
        
        self.get_logger().info("MOVING ROBOT NODE SUCCESSFULLY INITIATED")
        
        
    def process_command(self, msg):   
        if msg.command in self.move_commands:
            self.current_move_command = msg.command
            
            # setting requested_turn_angle 
            if msg.goal_angle > 5:
                self.current_requested_turn_angle = msg.goal_angle - self.turning_correction_angle
        else:
            self.get_logger().error("RECEIVED NON-EXISTENT MOVE COMMAND!") 
            
    
    def execute_command(self):
        if self.current_move_command in self.command_handlers:
            self.command_handlers[self.current_move_command]()      
            

    # keeps track of turning angle and stops robot when goal is reached
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
            
            # self.get_logger().info(f"Yaw accumulated: {math.degrees(self.yaw_accumulated):.2f}°")
            # self.get_logger().info(f"gyro_y: {msg.gyroscope_y} rad/s")

            # GOAL REACHED
            if abs(self.yaw_accumulated) >= math.radians(self.current_requested_turn_angle):
                self.stop_robot()
                self.current_requested_turn_angle = 0.0
                self.turning_right = False
                
        
    def stop_robot(self):
        self.reset_turning()
        self.reset_motor_speeds()
        
        command = Float32MultiArray()
        command.data = [self.current_left_speed, self.current_right_speed, self.current_servo_angle]
        self.motor_driver_commands_publisher.publish(command)
        
        self.current_move_command = ""
        
        
    def move_forwards_fast(self):
        self.reset_turning()
        
        self.current_left_speed = self.max_speed
        self.current_right_speed = self.max_speed
                
        command = Float32MultiArray()
        command.data = [self.current_left_speed, self.current_right_speed, self.current_servo_angle]
        self.motor_driver_commands_publisher.publish(command)


    def move_forwards_slow(self):
        self.reset_turning()
        
        self.current_left_speed = self.slow_speed
        self.current_right_speed = self.slow_speed
        
        command = Float32MultiArray()
        command.data = [self.current_left_speed, self.current_right_speed, self.current_servo_angle]
        self.motor_driver_commands_publisher.publish(command)


    def move_backwards_fast(self):
        self.reset_turning()
        
        self.current_left_speed = -self.max_speed
        self.current_right_speed = -self.max_speed
        
        command = Float32MultiArray()
        command.data = [self.current_left_speed, self.current_right_speed, self.current_servo_angle]
        self.motor_driver_commands_publisher.publish(command)


    def move_backwards_slow(self):
        self.reset_turning()
        
        self.current_left_speed = -self.slow_speed
        self.current_right_speed = -self.slow_speed
        
        command = Float32MultiArray()
        command.data = [self.current_left_speed, self.current_right_speed, self.current_servo_angle]
        self.motor_driver_commands_publisher.publish(command)


    def turn_left(self):
        self.yaw_accumulated = 0.0
        self.last_imu_time = self.get_clock().now()
        self.turning_left = True
        self.turning_right= False
        
        self.current_left_speed = -self.turning_speed
        self.current_right_speed = self.turning_speed

        command = Float32MultiArray()
        command.data = [self.current_left_speed, self.current_right_speed, self.current_servo_angle]
        self.motor_driver_commands_publisher.publish(command)
        
        self.current_move_command = ""   
           
                
    def turn_right(self):
        self.yaw_accumulated = 0.0
        self.last_imu_time = self.get_clock().now()
        self.turning_left = False
        self.turning_right = True

        self.current_left_speed = self.turning_speed
        self.current_right_speed = -self.turning_speed

        command = Float32MultiArray()
        command.data = [self.current_left_speed, self.current_right_speed, self.current_servo_angle]
        self.motor_driver_commands_publisher.publish(command)
        
        self.current_move_command = ""


    def head_straight(self):
        self.set_standard_head_angle()
        
        command = Float32MultiArray()
        command.data = [self.current_left_speed, self.current_right_speed, self.current_servo_angle]
        self.motor_driver_commands_publisher.publish(command)
        
        self.current_move_command = ""


    def head_left(self):
        self.set_standard_head_angle() 
        self.current_servo_angle = self.standard_servo_angle + 40
        
        command = Float32MultiArray()
        command.data = [self.current_left_speed, self.current_right_speed, self.current_servo_angle]
        self.motor_driver_commands_publisher.publish(command)
        
        self.current_move_command = ""
        
    
    def head_half_left(self):
        self.set_standard_head_angle() 
        self.current_servo_angle = self.standard_servo_angle + 20
        
        command = Float32MultiArray()
        command.data = [self.current_left_speed, self.current_right_speed, self.current_servo_angle]
        self.motor_driver_commands_publisher.publish(command)
        
        self.current_move_command = ""
        
        
    def head_right(self):
        self.set_standard_head_angle()
        self.current_servo_angle = self.standard_servo_angle - 40
        
        command = Float32MultiArray()
        command.data = [self.current_left_speed, self.current_right_speed, self.current_servo_angle]
        self.motor_driver_commands_publisher.publish(command)
        
        self.current_move_command = ""
        
        
    def head_half_right(self):
        self.set_standard_head_angle()
        self.current_servo_angle = self.standard_servo_angle - 20
        
        command = Float32MultiArray()
        command.data = [self.current_left_speed, self.current_right_speed, self.current_servo_angle]
        self.motor_driver_commands_publisher.publish(command)
        
        self.current_move_command = ""

    ########################
    ### ROBOT ANIMATIONS ###
    ########################
    
    def init_move(self):
        self.reset_turning()
        self.reset_motor_speeds()
        
        self.set_standard_head_angle()
        self.current_servo_angle += 20
        
        command = Float32MultiArray()
        command.data = [self.current_left_speed, self.current_right_speed, self.current_servo_angle]
        self.motor_driver_commands_publisher.publish(command)
        
        time.sleep(1.5)
        
        self.current_servo_angle = self.standard_servo_angle - 20
                
        command2 = Float32MultiArray()
        command2.data = [self.current_left_speed, self.current_right_speed, self.current_servo_angle]
        self.motor_driver_commands_publisher.publish(command2)
        
        time.sleep(2.0)
        
        self.set_standard_head_angle()
        
        command3 = Float32MultiArray()
        command3.data = [self.current_left_speed, self.current_right_speed, self.current_servo_angle]
        self.motor_driver_commands_publisher.publish(command3)
        
        self.current_move_command = ""
        

    def shake_head(self):
        self.set_standard_head_angle()
        self.current_servo_angle += 10
        
        command = Float32MultiArray()
        command.data = [self.current_left_speed, self.current_right_speed, self.current_servo_angle]
        self.motor_driver_commands_publisher.publish(command)
        
        time.sleep(0.2)
        
        self.current_servo_angle -= 22
        
        command2 = Float32MultiArray()
        command2.data = [self.current_left_speed, self.current_right_speed, self.current_servo_angle]
        self.motor_driver_commands_publisher.publish(command2)
        
        time.sleep(0.4)
        
        self.set_standard_head_angle()
        
        command3 = Float32MultiArray()
        command3.data = [self.current_left_speed, self.current_right_speed, self.current_servo_angle]
        self.motor_driver_commands_publisher.publish(command3)
        
        self.current_move_command = ""
        
        
        

    ########################
    ### HELPER FUNCTIONS ###
    ########################
        
    # standard head angle while driving for odometry with imu
    def set_standard_head_angle(self):
        self.current_servo_angle = self.standard_servo_angle
        
    # resetting motor speeds
    def reset_motor_speeds(self):
        self.current_left_speed = 0.0
        self.current_right_speed = 0.0    
    
    # stop turn when other command is received
    def reset_turning(self):
        self.turning_left = False
        self.turning_right= False        


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