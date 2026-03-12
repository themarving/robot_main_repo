### NODE PURPOSE ###
"""
creating subscriber for motor speed / servo angles and sending them motors / servos
also subscribes to IMU data and performs yaw-based compensation
"""
### NODE PURPOSE ###


#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
import serial
import time

# custom services and messages
from custom_interfaces.msg import IMUData

# ros2 topic pub /motor_driver_commands std_msgs/msg/Float32MultiArray "data: [-100.0, -100.0, 90.0, 90.0]"
# ros2 topic pub /motor_driver_commands std_msgs/msg/Float32MultiArray "data: [0.0, 0.0, 90.0, 90.0]"
# ros2 topic pub /motor_driver_commands std_msgs/msg/Float32MultiArray "data: [0.0, 0.0, 100.0, 80.0]"
# ros2 topic pub /motor_driver_commands std_msgs/msg/Float32MultiArray "data: [0.0, 0.0, 80.0, 100.0]"
# ros2 topic pub /motor_driver_commands std_msgs/msg/Float32MultiArray "data: [100.0, 100.0, 90.0, 90.0]"
# ros2 topic pub /motor_driver_commands std_msgs/msg/Float32MultiArray "data: [0.0, 0.0, 110.0, 70.0]"
# ros2 topic pub /motor_driver_commands std_msgs/msg/Float32MultiArray "data: [0.0, 0.0, 70.0, 110.0]"

# ros2 topic pub /motor_driver_commands std_msgs/msg/Float32MultiArray "data: [0.0, 0.0, 90.0, 90.0]"
# ros2 topic pub /motor_driver_commands std_msgs/msg/Float32MultiArray "data: [-220.0, -250.0, 90.0, 90.0]"
# ros2 topic pub /motor_driver_commands std_msgs/msg/Float32MultiArray "data: [-100.0, -125.0, 90.0, 90.0]"
# ros2 topic pub /motor_driver_commands std_msgs/msg/Float32MultiArray "data: [-125.0, 125.0, 90.0, 90.0]"


class MotorDriverCommsNode(Node):
    def __init__(self):
        super().__init__("motor_driver_comms_node")

        # Parameters for serial communication
        self.declare_parameter('serial_port', '/dev/ttyACM0')
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
        self.subscription  # prevent unused variable warning
        
        self.gyroscope_y = 0.0
        self.yaw_compensation = 0.0
        
        # imu data
        self.imu_data_subscriber = self.create_subscription(
            IMUData,
            'imu_data',
            self.process_imu_data,
            10
        )
        
        self.get_logger().info('MOTOR DRIVER COMMMS NODE SUCCESSFULLY INITIATED')


    def process_arduino_commands(self, msg):   
        if len(msg.data) != 4:
            self.get_logger().error('Received incorrect number of data elements. Required: 4')
            return

        # Extract data
        left_speed, right_speed, servo_left, servo_right = msg.data

        # Ensure motor speeds are between -255 and 255
        if left_speed < -255:
            left_speed = -255
        elif left_speed > 255:
            left_speed = 255

        if right_speed < -255:
            right_speed = -255
        elif right_speed > 255:
            right_speed = 255
            
        # constraining handled by arduino
        if servo_left < 0:
            servo_left = 0
        if servo_left > 180:
            servo_left = 180
            
        if servo_right < 0:
            servo_right = 0
        if servo_right > 180:
            servo_right = 180
        
        # adding yaw compensation
        # only needed if going forwards / backwards, not if turning
        if left_speed * right_speed > 0:  
            left_speed += self.yaw_compensation
            right_speed -= self.yaw_compensation

        left_speed = max(min(left_speed, 255.0), -255.0)
        right_speed = max(min(right_speed, 255.0), -255.0)

        # Create command string
        command = f'{left_speed:.2f},{right_speed:.2f},{servo_left:.2f},{servo_right:.2f}\n'
         
        # Send command to Arduino
        self.ser.write(command.encode())
        
        
    # IMU processing for yaw drift compensation
    def process_imu_data(self, msg):
        self.gyroscope_y = msg.gyroscope_y
        
        # if yaw is too small, we assume the robot is not turning
        yaw_deadzone = 0.02
        
        if abs(self.gyroscope_y) < yaw_deadzone:
            self.yaw_compensation = 0.0
            return

        # Calculate a correction based on yaw (rotation around Y axis).
        # Positive yaw means robot is rotating to the left
        correction = self.gyroscope_y * 100.0  # Gain factor; tune this for more/less correction

        self.yaw_compensation = correction


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