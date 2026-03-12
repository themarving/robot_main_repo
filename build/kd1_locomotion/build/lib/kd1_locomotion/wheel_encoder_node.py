### NODE PURPOSE ###
"""
getting wheel encoder data from motor encoders
"""
### NODE PURPOSE ###


#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int64MultiArray

import serial
import os
import time


class WheelEncoderNode(Node): 
    def __init__(self):
        super().__init__("wheel_encoder_node")

        # Get port from env var or parameter
        nano_port = os.getenv("NANO_PORT")
        self.declare_parameter('serial_port', nano_port)
        self.declare_parameter('baud_rate', 9600)

        serial_port = self.get_parameter('serial_port').get_parameter_value().string_value
        baud_rate = self.get_parameter('baud_rate').get_parameter_value().integer_value

        # Set up serial connection
        try:
            self.ser = serial.Serial(serial_port, baud_rate, timeout=1)
            time.sleep(2)  # Wait for Arduino to reset
            self.get_logger().info(f"Connected to encoder serial on {serial_port} @ {baud_rate}")
        except serial.SerialException as e:
            self.get_logger().error(f"Failed to connect to {serial_port}: {e}")
            raise e

        # ENCODER DATA PUBLISHER
        self.encoder_pub = self.create_publisher(Int64MultiArray, 'encoder_counts', 10)
        
        # TOF PUBLISHER
        self.tof_pub = self.create_publisher(Int64MultiArray, 'tof_distances_mm', 10)

        # Timer to poll serial
        self.timer = self.create_timer(0.05, self.read_serial)  # 20Hz

        self.get_logger().info("WHEEL ENCODER NODE SUCCESSFULLY INITIATED")


    def read_serial(self):
        if self.ser.in_waiting:
            try:
                line = self.ser.readline().decode('utf-8').strip()
                
                if line.startswith("ENC"):
                    parts = line.split()

                    if len(parts) == 6 and parts[3] == "TOF":
                        _, left_enc_str, right_enc_str, _, left_tof_str, right_tof_str = parts

                        # Parse encoder values
                        left_enc = -int(left_enc_str)  # Flip left encoder
                        right_enc = int(right_enc_str)
                        
                        # Publish encoder values
                        enc_msg = Int64MultiArray()
                        enc_msg.data = [left_enc, right_enc]
                        self.encoder_pub.publish(enc_msg)

                        # Parse TOF values
                        left_tof = int(left_tof_str)
                        right_tof = int(right_tof_str)

                        # Publish TOF values
                        tof_msg = Int64MultiArray()
                        tof_msg.data = [left_tof, right_tof]
                        self.tof_pub.publish(tof_msg)
                    else:
                        self.get_logger().warn(f"Incomplete or malformed line: {line}")
            except Exception as e:
                self.get_logger().warn(f"Error parsing serial line: {e}")
        
        
def main(args=None):
    rclpy.init(args=args)
    node = WheelEncoderNode() 
    
    try:
        rclpy.spin(node)
    finally:
        rclpy.shutdown()


if __name__ == "__main__":
    main()