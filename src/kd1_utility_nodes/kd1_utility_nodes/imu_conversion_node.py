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
        
        self.imu_is_calibrated = False
        self.calibration_count = 0
        
        # used for imu calibration, values from imu at rest
        self.accel_offset = {
            'x': 0.0,
            'y': 0.0, # 9.6989107131958
            'z': 0.0
        }

        self.gyro_offset = {
            'x': 0.0,
            'y': 0.0,
            'z': 0.0
        }
        
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
        
        
    # calibrating imu with imu values at rest
    def calibrate_imu(self, msg):
        self.accel_offset = {
            'x': -msg.accelerometer_x,
            'y': -msg.accelerometer_y,
            'z': -msg.accelerometer_z,
        }

        self.gyro_offset = {
            'x': -msg.gyroscope_x,
            'y': -msg.gyroscope_y,
            'z': -msg.gyroscope_z
        }
        
        self.calibration_count += 1
        
        if self.calibration_count == 10: 
            self.imu_is_calibrated = True
            self.get_logger().info("ROS2 IMU CALIBRATED SUCCESSFULLY")
        
        
    def process_imu_data(self, msg):
        if self.imu_is_calibrated:
            imu_msg = Imu()
            imu_msg.header.stamp = self.get_clock().now().to_msg()
            imu_msg.header.frame_id = 'imu_link'
            
            # removing imu offsets
            ax = msg.accelerometer_z + self.accel_offset['z']
            ay = msg.accelerometer_x + self.accel_offset['x']
            az = msg.accelerometer_y + self.accel_offset['y']

            gx = msg.gyroscope_z + self.gyro_offset['z']
            gy = msg.gyroscope_x + self.gyro_offset['x']
            gz = msg.gyroscope_y + self.gyro_offset['y']
            
            # cutting off gyro z-axis noise
            if gz < 0.01 and gz > -0.01:
                gz = 0.0

            imu_msg.linear_acceleration.x = ax
            imu_msg.linear_acceleration.y = ay
            imu_msg.linear_acceleration.z = az

            imu_msg.angular_velocity.x = gx
            imu_msg.angular_velocity.y = gy
            imu_msg.angular_velocity.z = gz


            imu_msg.orientation = Quaternion()
            imu_msg.orientation_covariance[0] = -1.0  # no orientation data

            # Linear acceleration covariance NOT USING FOR ROBOT LOCALIZATION
            imu_msg.linear_acceleration_covariance = [
                9999.99, 0.0, 0.0,   # x-axis: forward/backward, moderate trust, helps EKF correct small slips
                0.0, 9999.99, 0.0,   # y-axis: left/right, moderate trust, helps EKF correct small slips
                0.0, 0.0, 9999.99    # z-axis: up/down, very high covariance = ignore (robot moves mostly in XY plane)
            ]

            # Angular velocity covariance ONLY USING Z AXIS GYRO ACCELERATION
            imu_msg.angular_velocity_covariance = [
                9999.99, 0.0, 0.0,   # x-axis: roll, very high covariance = ignore
                0.0, 9999.99, 0.0,   # y-axis: pitch, very high covariance = ignore
                0.0, 0.0, 0.1        # z-axis: yaw, low covariance = trusted for rotation correction in EKF
            ]


            ### WORKING COVARIANCES ###
            # # Linear acceleration covariance
            # imu_msg.linear_acceleration_covariance = [
            #     0.05, 0.0, 0.0,   # x-axis: forward/backward, moderate trust, helps EKF correct small slips
            #     0.0, 0.05, 0.0,   # y-axis: left/right, moderate trust, helps EKF correct small slips
            #     0.0, 0.0, 0.05    # z-axis: up/down, very high covariance = ignore (robot moves mostly in XY plane)
            # ]

            # # Angular velocity covariance
            # imu_msg.angular_velocity_covariance = [
            #     0.05, 0.0, 0.0,   # x-axis: roll, very high covariance = ignore
            #     0.0, 0.05, 0.0,   # y-axis: pitch, very high covariance = ignore
            #     0.0, 0.0, 0.05    # z-axis: yaw, low covariance = trusted for rotation correction in EKF
            # ]
            ### WORKING COVARIANCES ###
            
            self.imu_data_publisher.publish(imu_msg)
        else:
            self.calibrate_imu(msg)


def main(args=None):
    rclpy.init(args=args)                    
    node = IMUConversionNode()             
    try:
        rclpy.spin(node)                     
    finally:
        rclpy.shutdown()                   

if __name__ == '__main__':
    main()