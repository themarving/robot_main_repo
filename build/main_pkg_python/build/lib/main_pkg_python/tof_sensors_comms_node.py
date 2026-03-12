### NODE PURPOSE ###
"""
publishing tof sensor data for distance measurements
"""
### NODE PURPOSE ###


#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
import serial
import time

# using custom msg type
from custom_interfaces.msg import TOFSensorData 


class TOFSensorCommsNode(Node):
    def __init__(self):
        super().__init__("tof_sensors_comms_node")

        # Set up the serial connection to the Arduino Nano Every
        self.ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)  # Adjust the port if necessary

        # Create a publisher for the custom message
        self.sensor_data_publisher = self.create_publisher(TOFSensorData, 'tof_sensor_data', 10)

        # Timer to read the serial data
        self.timer = self.create_timer(0.05, self.read_serial_data)
        
        self.get_logger().info("TOF SENSORS COMMS NODE SUCCESSFULLY INITIATED")
        
        
    def reset_serial_connection(self):
        try:
            self.get_logger().warn("Resetting serial connection due to 65535.0 value.")
            self.ser.close()  # Close the serial connection
            self.ser.open()   # Reopen the serial connection

            self.ser.setDTR(False)  # Disable DTR (this will reset the Arduino)
            time.sleep(0.1)         # Wait for a short period
            self.ser.setDTR(True)   # Enable DTR again
            
            self.get_logger().info("Serial connection successfully reset.")
            
        except Exception as e:
            self.get_logger().error(f"Failed to reset serial connection: {e}")


    def read_serial_data(self):
        # Check if data is available on the serial port
        if self.ser.in_waiting > 0:
            # Read the serial data (assuming Arduino sends comma-separated values)
            data = self.ser.readline().decode('utf-8').strip()

            if data:
                # Split the comma-separated values
                sensor_values = data.split(", ")

                # Ensure there are four values (one for each sensor)
                if len(sensor_values) == 4:
                    # Convert the string values to float
                    front_left = float(sensor_values[0])
                    front_right = float(sensor_values[1])
                    mid_left = float(sensor_values[2])
                    mid_right = float(sensor_values[3])
                    
                    # if any value is 65535.0 (bad sensor reads) then reset the serial connection
                    if (front_left == 65535.0 or front_right == 65535.0 or mid_left == 65535.0 or mid_right == 65535.0):
                        self.reset_serial_connection()
                        return

                    # Create and publish the custom message
                    msg = TOFSensorData()
                    
                    msg.front_left = front_left
                    msg.front_right = front_right
                    msg.mid_left = mid_left
                    msg.mid_right = mid_right
                    
                    self.sensor_data_publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = TOFSensorCommsNode()

    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()