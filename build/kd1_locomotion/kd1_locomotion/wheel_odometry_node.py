### NODE PURPOSE ###
"""
turning wheel encoder data into wheel odometry (linear acceleration x and angular velocity z)
"""
### NODE PURPOSE ###

#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int64MultiArray  
from nav_msgs.msg import Odometry      
from sensor_msgs.msg import JointState
import math


class WheelOdometryNode(Node):
    def __init__(self):
        super().__init__('wheel_odometry_node')
        
        # joint_states for rviz
        self.joint_state_pub = self.create_publisher(JointState, 'joint_states', 10)
        self.left_position = 0.0
        self.right_position = 0.0

        # Declare parameters with default values; users can override via ROS params
        self.declare_parameter('ticks_per_revolution', 880) # 1760, 1320    # (reduction rate * pulses per single phase * 4) 40 * 11 * 4 - Encoder ticks per wheel revolution
        self.declare_parameter('wheel_diameter_m', 0.065)        # Diameter of wheel in meters (65 mm)
        self.declare_parameter('wheel_base_m', 0.245)             # Distance between left and right wheels (wheelbase)

        # Get parameter values
        self.ticks_per_rev = self.get_parameter('ticks_per_revolution').get_parameter_value().integer_value
        self.wheel_diameter = self.get_parameter('wheel_diameter_m').get_parameter_value().double_value
        self.wheel_base = self.get_parameter('wheel_base_m').get_parameter_value().double_value

        # Calculate wheel circumference for distance conversions
        self.wheel_circumference = self.wheel_diameter * math.pi

        # Variables to store previous encoder readings and time for delta calculations
        self.last_left_ticks = None
        self.last_right_ticks = None
        self.last_time = None

        # Subscribe to encoder ticks published on 'encoder_counts' topic
        # Expecting Int64MultiArray with [left_ticks, right_ticks]
        self.create_subscription(
            Int64MultiArray, 
            'encoder_counts', 
            self.encoder_callback, 
            10
        )

        # Publisher for odometry output, publishing computed pose and velocity
        # Topic name: 'wheel_encoder_odom' to distinguish from fused odometry (/odom)
        self.odom_pub = self.create_publisher(
            Odometry, 
            'wheel_encoder_odom', 
            10
        )

        self.get_logger().info("WHEEL ODOMETRY NODE SUCCESSFULLY INITIATED")
        

    def encoder_callback(self, msg):
        # If the encoder message does not contain at least 2 values (left, right ticks), skip
        if len(msg.data) < 2:
            self.get_logger().warn("Encoder data length less than 2")
            return

        # Unpack the current encoder tick counts
        left_ticks, right_ticks = msg.data
        # Record the current ROS time for timing calculations
        now = self.get_clock().now()

        # If this is the first time receiving encoder data, store values and return
        # (We can't calculate velocity without a previous reading)
        if self.last_left_ticks is None:
            self.last_left_ticks = left_ticks
            self.last_right_ticks = right_ticks
            self.last_time = now
            return

        # Calculate how many ticks each wheel moved since the last reading
        delta_left = left_ticks - self.last_left_ticks
        delta_right = right_ticks - self.last_right_ticks
        # Update stored tick counts for the next callback
        self.last_left_ticks = left_ticks
        self.last_right_ticks = right_ticks

        # Calculate the time elapsed (in seconds) since the last reading
        dt = (now - self.last_time).nanoseconds * 1e-9
        if dt == 0:
            # If no time has passed (shouldn't happen under normal conditions), skip
            return
        # Update the last time stamp for the next cycle
        self.last_time = now

        # Convert one tick count to physical distance traveled (m/tick)
        dist_per_tick = self.wheel_circumference / self.ticks_per_rev
        # Convert tick deltas to meters moved per wheel
        d_left = delta_left * dist_per_tick
        d_right = delta_right * dist_per_tick

        # --- Compute Wheel Velocities ---
        # Velocity of each wheel (m/s)
        v_left = d_left / dt
        v_right = d_right / dt
        # Forward velocity of robot = average of both wheel velocities
        v_center = (v_left + v_right) / 2.0
        # Angular velocity around z-axis (rad/s) from wheel speed difference
        v_theta = (v_right - v_left) / self.wheel_base

        # --- Prepare Odometry Message ---
        odom_msg = Odometry()
        odom_msg.header.stamp = now.to_msg()        # Set timestamp
        odom_msg.header.frame_id = "odom"           # Reference frame for velocities
        odom_msg.child_frame_id = "base_link"       # Robot's base frame

        # Only velocity is filled; no position is calculated here
        odom_msg.twist.twist.linear.x = v_center    # Forward velocity
        odom_msg.twist.twist.linear.y = 0.0         # No sideways movement (diff drive)
        odom_msg.twist.twist.angular.z = v_theta    # Yaw rate

        # --- Wheel Odometry Twist Covariance ---
        # 6×6 matrix, flattened row-major, each row describes the uncertainty for:
        # Row 0 → x-axis linear velocity (vx)
        # Row 1 → y-axis linear velocity (vy)
        # Row 2 → z-axis linear velocity (vz)
        # Row 3 → x-axis angular velocity (wx, roll rate)
        # Row 4 → y-axis angular velocity (wy, pitch rate)
        # Row 5 → z-axis angular velocity (wz, yaw rate)
        odom_msg.twist.covariance = [
            0.15, 0.0, 0.0, 0.0, 0.0, 0.0,       # Row 0: vx covariance row USING
            0.0, 99999.0, 0.0, 0.0, 0.0, 0.0,    # Row 1: vy covariance row
            0.0, 0.0, 99999.0, 0.0, 0.0, 0.0,    # Row 2: vz covariance row
            0.0, 0.0, 0.0, 99999.0, 0.0, 0.0,    # Row 3: wx covariance row
            0.0, 0.0, 0.0, 0.0, 99999.0, 0.0,    # Row 4: wy covariance row
            0.0, 0.0, 0.0, 0.0, 0.0, 0.15        # Row 5: wz covariance row USING BUT TRUSTING LESS THAN IMU Z ACCELERATION
        ] 


        # ### WORKING COVARIANCE ###
        # odom_msg.pose.covariance = [
        #     0.01, 0.0, 0.0, 0.0, 0.0, 0.0,
        #     0.0, 0.01, 0.0, 0.0, 0.0, 0.0,
        #     0.0, 0.0, 99999.0, 0.0, 0.0, 0.0,
        #     0.0, 0.0, 0.0, 99999.0, 0.0, 0.0,
        #     0.0, 0.0, 0.0, 0.0, 99999.0, 0.0,
        #     0.0, 0.0, 0.0, 0.0, 0.0, 0.15
        # ]

        # odom_msg.twist.covariance = [
        #     0.1, 0.0, 0.0, 0.0, 0.0, 0.0,
        #     0.0, 0.1, 0.0, 0.0, 0.0, 0.0,
        #     0.0, 0.0, 99999.0, 0.0, 0.0, 0.0,
        #     0.0, 0.0, 0.0, 99999.0, 0.0, 0.0,
        #     0.0, 0.0, 0.0, 0.0, 99999.0, 0.0,
        #     0.0, 0.0, 0.0, 0.0, 0.0, 0.15
        # ]
        # ### WORKING COVARIANCE ###
        
        
        # Publish odometry on 'wheel_encoder_odom'
        self.odom_pub.publish(odom_msg)
        
        # Update joint positions (accumulated radians)
        self.left_position += (delta_left * 2 * math.pi) / self.ticks_per_rev
        self.right_position += (delta_right * 2 * math.pi) / self.ticks_per_rev

        # Publish JointState
        joint_state_msg = JointState()
        joint_state_msg.header.stamp = now.to_msg()
        joint_state_msg.name = ["left_wheel_joint", "right_wheel_joint"]
        joint_state_msg.position = [self.left_position, self.right_position]
        self.joint_state_pub.publish(joint_state_msg)


def main(args=None):
    rclpy.init(args=args)                    
    node = WheelOdometryNode()             
    try:
        rclpy.spin(node)                     
    finally:
        rclpy.shutdown()                   

if __name__ == '__main__':
    main()