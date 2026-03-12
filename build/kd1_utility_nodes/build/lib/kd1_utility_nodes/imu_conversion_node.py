### NODE PURPOSE ###
"""
converting custom imu msg type into standard ros imu msg type
"""
### NODE PURPOSE ###

#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Imu
from custom_interfaces.msg import IMUData
from geometry_msgs.msg import Quaternion

# raw imu
# z is forward,
# y is up,
# x is right

class IMUConversionNode(Node):
    def __init__(self):
        super().__init__('imu_conversion_node')
        
        self.alpha = 0.1  # smoothing factor, adjust for more or less smoothing
        
        # Initialize filtered values to zero or None
        self.filtered_accel = {'x': 0.0, 'y': 0.0, 'z': 0.0}
        self.filtered_gyro = {'x': 0.0, 'y': 0.0, 'z': 0.0}
        
        # imu data
        self.imu_data_subscriber = self.create_subscription(
            IMUData,
            'imu_data',
            self.process_imu_data,
            10
        )
        
        self.imu_data_publisher = self.create_publisher(
            Imu,
            'imu_ros2_compatible',
            10
        )

        self.get_logger().info("IMU CONVERSION NODE SUCCESSFULLY INITIATED")
        
    def process_imu_data(self, msg):
        imu_msg = Imu()
        imu_msg.header.stamp = self.get_clock().now().to_msg()
        imu_msg.header.frame_id = 'imu_link'

        # Apply low-pass filter to accelerometer
        self.filtered_accel['x'] = self.alpha * msg.accelerometer_z + (1 - self.alpha) * self.filtered_accel['x']
        self.filtered_accel['y'] = self.alpha * msg.accelerometer_x + (1 - self.alpha) * self.filtered_accel['y']
        self.filtered_accel['z'] = self.alpha * msg.accelerometer_y + (1 - self.alpha) * self.filtered_accel['z']

        imu_msg.linear_acceleration.x = self.filtered_accel['x']
        imu_msg.linear_acceleration.y = self.filtered_accel['y']
        imu_msg.linear_acceleration.z = self.filtered_accel['z']

        # Apply low-pass filter to gyroscope
        self.filtered_gyro['x'] = self.alpha * msg.gyroscope_z + (1 - self.alpha) * self.filtered_gyro['x']
        self.filtered_gyro['y'] = self.alpha * msg.gyroscope_x + (1 - self.alpha) * self.filtered_gyro['y']
        self.filtered_gyro['z'] = self.alpha * msg.gyroscope_y + (1 - self.alpha) * self.filtered_gyro['z']

        imu_msg.angular_velocity.x = self.filtered_gyro['x']
        imu_msg.angular_velocity.y = self.filtered_gyro['y']
        imu_msg.angular_velocity.z = self.filtered_gyro['z']

        imu_msg.orientation = Quaternion()
        imu_msg.orientation_covariance[0] = -1.0  # no orientation data

        imu_msg.linear_acceleration_covariance = [
            0.05, 0.0, 0.0, # x
            0.0, 0.05, 0.0, # y
            0.0, 0.0, 0.05 # z
        ]

        imu_msg.angular_velocity_covariance = [
            0.05, 0.0, 0.0,
            0.0, 0.05, 0.0,
            0.0, 0.0, 0.05
        ]
        
        
        # ### WORKING COVARIANCE ###
        # imu_msg.linear_acceleration_covariance = [
        #     0.05, 0.0, 0.0,
        #     0.0, 0.05, 0.0,
        #     0.0, 0.0, 0.05
        # ]

        # imu_msg.angular_velocity_covariance = [
        #     0.05, 0.0, 0.0,
        #     0.0, 0.05, 0.0,
        #     0.0, 0.0, 0.05
        # ]
        # ### WORKING COVARIANCE ###


        self.imu_data_publisher.publish(imu_msg)

def main(args=None):
    rclpy.init(args=args)                    
    node = IMUConversionNode()             
    try:
        rclpy.spin(node)                     
    finally:
        rclpy.shutdown()                   

if __name__ == '__main__':
    main()