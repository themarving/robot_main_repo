### NODE PURPOSE ###
"""
getting wheel encoder data from motor encoders and tof data
"""
### NODE PURPOSE ###


#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int64MultiArray
from sensor_msgs.msg import Range

import serial
import os
import time


class WheelEncoderTOFNode(Node): 
    def __init__(self):
        super().__init__("wheel_encoder_tof_node")

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
        self.encoder_pub = self.create_publisher(
            Int64MultiArray, 
            'encoder_counts', 
            10
        )
        
        # PUBLISHERS FOR EACH TOF SENSOR
        self.tof_front_left_pub = self.create_publisher(Range, 'tof_front_left', 10)
        self.tof_front_right_pub = self.create_publisher(Range, 'tof_front_right', 10)
        self.tof_back_left_pub = self.create_publisher(Range, 'tof_back_left', 10)
        self.tof_back_right_pub = self.create_publisher(Range, 'tof_back_right', 10)
        
        # Range sensor settings
        self.min_range = 0.03  # meters
        self.max_range = 1.0   # meters
        self.field_of_view = 0.2  # radians (~11°)
        self.tof_front_left_correction = -0.0 # TO-DO: ranges 0.055 m MORE than real life
        self.tof_front_right_correction = -0.0 # TO-DO: ranges 0.02 m MORE than real life
        self.tof_back_left_correction = -0.0 # TO-DO: ranges 0.055 m MORE than real life
        self.tof_back_right_correction = -0.0 # TO-DO: ranges 0.02 m MORE than real life
        
        # Timer to poll serial
        self.timer = self.create_timer(0.05, self.read_serial)  # 20Hz

        self.get_logger().info("WHEEL ENCODER AND TOF NODE SUCCESSFULLY INITIATED")
        
        
    def create_range_msg(self, frame_id, distance_m):
        msg = Range()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = frame_id
        msg.radiation_type = Range.INFRARED  # ALTERNATIVE: Range.ULTRASOUND 
        msg.field_of_view = self.field_of_view
        msg.min_range = self.min_range
        msg.max_range = self.max_range
        msg.range = float(distance_m)
        return msg


    def read_serial(self):
        if self.ser.in_waiting:
            try:
                line = self.ser.readline().decode('utf-8').strip()

                if line.startswith("ENC"):
                    parts = line.split()

                    if len(parts) == 8 and parts[3] == "TOF":
                        _, left_enc_str, right_enc_str, _, front_left_tof_str, front_right_tof_str, back_left_tof_str, back_right_tof_str  = parts

                        # Parse encoder values
                        left_enc = int(left_enc_str)  
                        right_enc = -int(right_enc_str) # inverted encoder
                        
                        # Publish encoder values
                        enc_msg = Int64MultiArray()
                        enc_msg.data = [left_enc, right_enc]
                        self.encoder_pub.publish(enc_msg)

                        # TOF
                        # Convert mm to meters
                        front_left_m = float(front_left_tof_str) / 1000.0
                        front_right_m = float(front_right_tof_str) / 1000.0
                        back_left_m = float(back_left_tof_str) / 1000.0
                        back_right_m = float(back_right_tof_str) / 1000.0
                        
                        # adding correction values
                        front_left_m+=self.tof_front_left_correction
                        front_right_m+=self.tof_front_right_correction
                        back_left_m+=self.tof_back_left_correction
                        back_right_m+=self.tof_back_right_correction

                        # Clamp to min/max range
                        front_left_m = min(max(front_left_m, self.min_range), self.max_range)
                        front_right_m = min(max(front_right_m, self.min_range), self.max_range)
                        back_left_m = min(max(back_left_m, self.min_range), self.max_range)
                        back_right_m = min(max(back_right_m, self.min_range), self.max_range)

                        # Create and publish Range messages
                        front_left_msg = self.create_range_msg('tof_front_left_link', front_left_m)
                        front_right_msg = self.create_range_msg('tof_front_right_link', front_right_m)
                        back_left_msg = self.create_range_msg('tof_back_left_link', back_left_m)
                        back_right_msg = self.create_range_msg('tof_back_right_link', back_right_m)

                        self.tof_front_left_pub.publish(front_left_msg)
                        self.tof_front_right_pub.publish(front_right_msg)
                        self.tof_back_left_pub.publish(back_left_msg)
                        self.tof_back_right_pub.publish(back_right_msg)
                    else:
                        self.get_logger().warn(f"Incomplete or malformed line: {line}")
            except Exception as e:
                self.get_logger().warn(f"Error parsing serial line: {e}")
        
        
def main(args=None):
    rclpy.init(args=args)
    node = WheelEncoderTOFNode() 
    
    try:
        rclpy.spin(node)
    finally:
        rclpy.shutdown()


if __name__ == "__main__":
    main()