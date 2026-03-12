### NODE PURPOSE ###
"""
creating subscriber for motor speed / servo angles and sending them motors / servos
also subscribes to IMU data and performs yaw-based compensation
also subscribes to robot_lights_command which controls the robot's big lights
"""
### NODE PURPOSE ###


#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray, String

import os
import serial
import time

# custom services and messages
from custom_interfaces.msg import IMUData

# ros2 topic pub /motor_driver_commands std_msgs/msg/Float32MultiArray "data: [-255.0, -255.0, 90.0]" --once
# ros2 topic pub /motor_driver_commands std_msgs/msg/Float32MultiArray "data: [0.0, 0.0, 70.0]" --once
# ros2 topic pub /motor_driver_commands std_msgs/msg/Float32MultiArray "data: [0.0, -100.0, 100.0]"
# ros2 topic pub /motor_driver_commands std_msgs/msg/Float32MultiArray "data: [0.0, 0.0, 110.0]"
# ros2 topic pub /motor_driver_commands std_msgs/msg/Float32MultiArray "data: [100.0, 100.0, 90.0]"
# ros2 topic pub /motor_driver_commands std_msgs/msg/Float32MultiArray "data: [0.0, 0.0, 110.0]"
# ros2 topic pub /motor_driver_commands std_msgs/msg/Float32MultiArray "data: [0.0, 0.0, 70.0]"

# ros2 topic pub /motor_driver_commands std_msgs/msg/Float32MultiArray "data: [0.0, 0.0, 90.0]"
# ros2 topic pub /motor_driver_commands std_msgs/msg/Float32MultiArray "data: [-220.0, -250.0, 90.0]"
# ros2 topic pub /motor_driver_commands std_msgs/msg/Float32MultiArray "data: [-100.0, -125.0, 90.0]"
# ros2 topic pub /motor_driver_commands std_msgs/msg/Float32MultiArray "data: [-125.0, 125.0, 90.0]"

# ros2 topic pub /robot_lights_command std_msgs/msg/String "data: 'blueWhiteOn'"


class MotorDriverCommsNode(Node):
    def __init__(self):
        super().__init__("motor_driver_comms_node")
        
        uno_port = os.getenv("UNO_PORT")

        # Parameters for serial communication
        self.declare_parameter('serial_port', uno_port)
        self.declare_parameter('baud_rate', 9600)

        serial_port = self.get_parameter('serial_port').get_parameter_value().string_value
        baud_rate = self.get_parameter('baud_rate').get_parameter_value().integer_value

        # Initialize serial communication to Arduino Uno
        self.ser = serial.Serial(serial_port, baud_rate, timeout = 1)
        time.sleep(2)  # Wait for Arduino to reset

        # Subscriber to receive motor commands
        self.subscription = self.create_subscription(
            Float32MultiArray,
            'motor_driver_commands',
            self.process_arduino_commands,
            10
        )
        
        self.current_left_speed = 0.0
        self.current_right_speed = 0.0
        self.current_servo_angle = 90.0
        
        self.gain_factor = 270 # adjust for gain
        self.gyroscope_y = 0.0
        self.yaw_compensation = 0.0
        self.yaw_clamping = 30
        
        # at what pwm difference should the yaw compensation kick in
        self.speed_diff_threshold = 30.0
        self.max_speed_in_pwm = 255
        
        # imu data
        self.imu_data_subscriber = self.create_subscription(
            IMUData,
            'imu_data',
            self.process_imu_data,
            10
        )
        
        # light_command subscriber
        self.subscription = self.create_subscription(
            String,
            'robot_lights_command',
            self.update_light_command,
            10
        )
        
        # controlling the robot lights
        # available commands -> blueOn, whiteOn, blueWhiteOn, off
        self.light_command = "blueOn"
        
        self.get_logger().info('MOTOR DRIVER COMMMS NODE SUCCESSFULLY INITIATED')


    def process_arduino_commands(self, msg):   
        if len(msg.data) != 3:
            self.get_logger().error('Received incorrect number of data elements. Required: 3')
            return

        # Extract data
        left_speed, right_speed, servo_angle = msg.data

        # Ensure motor speeds are between -255 and 255
        if left_speed < -self.max_speed_in_pwm:
            left_speed = -self.max_speed_in_pwm
        elif left_speed > self.max_speed_in_pwm:
            left_speed = self.max_speed_in_pwm

        if right_speed < -self.max_speed_in_pwm:
            right_speed = -self.max_speed_in_pwm
        elif right_speed > self.max_speed_in_pwm:
            right_speed = self.max_speed_in_pwm
            
        # constraining handled by arduino
        if servo_angle < 0:
            servo_angle = 0
        if servo_angle > 180:
            servo_angle = 180
            
        self.current_servo_angle = servo_angle
            
        # Clamp yaw compensation between values
        self.yaw_compensation = max(-self.yaw_clamping, min(self.yaw_clamping, self.yaw_compensation))
        
        # adding yaw compensation
        # only needed if going forwards / backwards, not if turning
        if left_speed * right_speed > 0 and abs(left_speed - right_speed) <= self.speed_diff_threshold:
            left_speed += self.yaw_compensation 
            right_speed -= self.yaw_compensation 
            
            # self.get_logger().info(
            #     f"Compensation: {self.yaw_compensation:.2f}, "
            #     f"Left PWM: {left_speed:.2f}, Right PWM: {right_speed:.2f}"
            # )

        self.current_left_speed = max(min(left_speed, self.max_speed_in_pwm), -self.max_speed_in_pwm)
        self.current_right_speed = max(min(right_speed, self.max_speed_in_pwm), -self.max_speed_in_pwm)

        # Create command string
        command = f'{self.current_left_speed:.2f},{self.current_right_speed:.2f},{self.current_servo_angle:.2f},{self.light_command}\n'
        
        # Send command to Arduino
        self.ser.write(command.encode())
        
        
    # IMU processing for yaw drift compensation
    def process_imu_data(self, msg):
        self.gyroscope_y = msg.gyroscope_y
        
        # if yaw is too small, we assume the robot is not turning
        yaw_deadzone = 0.01
        
        if abs(self.gyroscope_y) < yaw_deadzone:
            self.yaw_compensation = 0.0
            return

        # Calculate a correction based on yaw (rotation around Y axis).
        # Positive yaw means robot is rotating to the left
        correction = self.gyroscope_y * self.gain_factor  # Gain factor; tune this for more/less correction

        self.yaw_compensation = correction
        
    
    def update_light_command(self, msg):
        self.light_command = msg.data
        
        command = f'{self.current_left_speed:.2f},{self.current_right_speed:.2f},{self.current_servo_angle:.2f},{self.light_command}\n'
        self.ser.write(command.encode())


def main(args=None):
    rclpy.init(args=args)
    node = MotorDriverCommsNode()
    
    try:
        rclpy.spin(node)
    finally:
        # cleanup
        node.ser.close()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()