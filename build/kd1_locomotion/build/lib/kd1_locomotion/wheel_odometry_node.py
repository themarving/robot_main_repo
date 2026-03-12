### NODE PURPOSE ###
"""
turning wheel encoder data into wheel odometry
"""
### NODE PURPOSE ###

#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int64MultiArray  
from nav_msgs.msg import Odometry      
from sensor_msgs.msg import JointState
from geometry_msgs.msg import Quaternion  
import math


class WheelOdometryNode(Node):
    def __init__(self):
        super().__init__('wheel_odometry_node')
        
        # joint_states for rviz
        self.joint_state_pub = self.create_publisher(JointState, 'joint_states', 10)
        self.left_position = 0.0
        self.right_position = 0.0

        # Declare parameters with default values; users can override via ROS params
        self.declare_parameter('ticks_per_revolution', 1220) # 1440    # Encoder ticks per wheel revolution
        self.declare_parameter('wheel_diameter_m', 0.065)        # Diameter of wheel in meters (65 mm)
        self.declare_parameter('wheel_base_m', 0.32)             # Distance between left and right wheels (wheelbase)

        # Get parameter values
        self.ticks_per_rev = self.get_parameter('ticks_per_revolution').get_parameter_value().integer_value
        self.wheel_diameter = self.get_parameter('wheel_diameter_m').get_parameter_value().double_value
        self.wheel_base = self.get_parameter('wheel_base_m').get_parameter_value().double_value

        # Calculate wheel circumference for distance conversions
        self.wheel_circumference = self.wheel_diameter * math.pi

        # Initialize robot pose (x, y, theta)
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0  # Yaw angle in radians

        # Variables to store previous encoder readings and time for delta calculations
        self.last_left_ticks = None
        self.last_right_ticks = None
        self.last_time = None

        # Subscribe to encoder ticks published on 'encoder_counts' topic
        # Expecting Int64MultiArray with [left_ticks, right_ticks]
        self.create_subscription(Int64MultiArray, 'encoder_counts', self.encoder_callback, 10)

        # Publisher for odometry output, publishing computed pose and velocity
        # Topic name: 'wheel_encoder_odom' to distinguish from fused odometry (/odom)
        self.odom_pub = self.create_publisher(Odometry, 'wheel_encoder_odom', 10)
        
        # Subscribe filtered odometry to get better pose estimates
        self.filtered_odom_sub = self.create_subscription(
            Odometry,
            '/odometry/filtered',  
            self.filtered_odom_callback,
            10
        )
        
        # Store last received filtered odom pose and orientation (init to None)
        self.filtered_pose = None
        self.filtered_orientation = None
        
        # Timer to reset wheel odometry pose every interval 
        self.reset_timer = self.create_timer(2.0, self.reset_pose_to_filtered)

        self.get_logger().info("WHEEL ODOMETRY NODE SUCCESSFULLY INITIATED")
        
    # TURNING WHEEL ODOM TO FILTERED ODOM IN INTERVALS TO REMOVE WHEEL SLIPPAGE
    def filtered_odom_callback(self, msg: Odometry):
        # Store filtered odometry pose and orientation for periodic reset
        self.filtered_pose = msg.pose.pose.position
        self.filtered_orientation = msg.pose.pose.orientation
        
    def reset_pose_to_filtered(self):
        # If we have filtered odometry, reset internal pose to it
        if self.filtered_pose is None or self.filtered_orientation is None:
            return

        # Reset x, y from filtered pose
        self.x = self.filtered_pose.x
        self.y = self.filtered_pose.y

        # Convert quaternion to yaw (theta)
        self.theta = self.quaternion_to_yaw(self.filtered_orientation)


    def encoder_callback(self, msg: Int64MultiArray):
        # This callback runs when new encoder data arrives

        # Validate message length
        if len(msg.data) < 2:
            self.get_logger().warn("Encoder data length less than 2")
            return

        # Extract current encoder ticks for left and right wheels
        left_ticks = msg.data[0]
        right_ticks = msg.data[1]

        # Current time (ROS time)
        now = self.get_clock().now()

        # On first message, just store ticks and time to compute deltas on next call
        if self.last_left_ticks is None or self.last_right_ticks is None:
            self.last_left_ticks = left_ticks
            self.last_right_ticks = right_ticks
            self.last_time = now
            return

        # Calculate change in ticks since last message
        delta_left = left_ticks - self.last_left_ticks
        delta_right = right_ticks - self.last_right_ticks

        # Update stored last ticks for next callback
        self.last_left_ticks = left_ticks
        self.last_right_ticks = right_ticks

        # Calculate time difference (in seconds) between messages
        dt = (now - self.last_time).nanoseconds * 1e-9
        if dt == 0:
            self.get_logger().warn("Zero dt, skipping update")
            return
        self.last_time = now

        # Convert tick counts to linear distance traveled by each wheel
        dist_per_tick = self.wheel_circumference / self.ticks_per_rev
        d_left = delta_left * dist_per_tick
        d_right = delta_right * dist_per_tick

        # Calculate robot's linear and angular displacement
        d_center = (d_left + d_right) / 2.0            # Average forward distance
        d_theta = (d_right - d_left) / self.wheel_base  # Change in orientation (yaw)

        # Calculate change in position (dx, dy) in robot frame, considering arc movement
        if d_theta != 0:
            # Robot moved along an arc of radius r
            r = d_center / d_theta
            dx = r * math.sin(d_theta)
            dy = r * (1 - math.cos(d_theta))
        else:
            # Robot moved straight forward
            dx = d_center
            dy = 0

        # Transform dx, dy from robot frame to odom/world frame
        cos_theta = math.cos(self.theta)
        sin_theta = math.sin(self.theta)
        self.x += cos_theta * dx - sin_theta * dy
        self.y += sin_theta * dx + cos_theta * dy
        self.theta += d_theta

        # Normalize theta to [-pi, pi]
        self.theta = (self.theta + math.pi) % (2 * math.pi) - math.pi

        # Calculate velocities based on displacements and elapsed time
        vx = d_center / dt     # Linear velocity (m/s)
        vth = d_theta / dt     # Angular velocity (rad/s)

        # Prepare and publish odometry message
        odom_msg = Odometry()
        odom_msg.header.stamp = now.to_msg()          # Timestamp of current reading
        odom_msg.header.frame_id = "odom"              # Fixed world frame
        odom_msg.child_frame_id = "base_link"          # Robot base frame

        # Fill position
        odom_msg.pose.pose.position.x = self.x
        odom_msg.pose.pose.position.y = self.y
        odom_msg.pose.pose.position.z = 0.0

        # Convert yaw to quaternion for orientation
        q = self.yaw_to_quaternion(self.theta)
        odom_msg.pose.pose.orientation = q

        # Fill velocity
        odom_msg.twist.twist.linear.x = vx
        odom_msg.twist.twist.angular.z = vth
        
        # Pose covariance (x, y, z, roll, pitch, yaw)
        # Assuming no z or roll/pitch change, yaw uncertainty small but nonzero
        odom_msg.pose.covariance = [
            0.15, 0.0, 0.0, 0.0, 0.0, 0.0, # x
            0.0, 0.15, 0.0, 0.0, 0.0, 0.0, # y
            0.0, 0.0, 99999.0, 0.0, 0.0, 0.0, # z
            0.0, 0.0, 0.0, 99999.0, 0.0, 0.0, # roll
            0.0, 0.0, 0.0, 0.0, 99999.0, 0.0, # pitch
            0.0, 0.0, 0.0, 0.0, 0.0, 0.15 # yaw
        ]

        odom_msg.twist.covariance = [
            0.15, 0.0, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.15, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 99999.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 99999.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0, 99999.0, 0.0,
            0.0, 0.0, 0.0, 0.0, 0.0, 0.15
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
        
        
    def yaw_to_quaternion(self, yaw):
        q = Quaternion()
        q.w = math.cos(yaw / 2.0)
        q.x = 0.0
        q.y = 0.0
        q.z = math.sin(yaw / 2.0)
        return q

    def quaternion_to_yaw(self, q):
        # Convert geometry_msgs.msg.Quaternion to yaw angle (radians)
        siny_cosp = 2.0 * (q.w * q.z + q.x * q.y)
        cosy_cosp = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
        yaw = math.atan2(siny_cosp, cosy_cosp)
        return yaw


    def yaw_to_quaternion(self, yaw):
        # Helper function to convert yaw angle to quaternion
        q = Quaternion()
        q.w = math.cos(yaw / 2.0)
        q.x = 0.0
        q.y = 0.0
        q.z = math.sin(yaw / 2.0)
        return q


def main(args=None):
    rclpy.init(args=args)                    
    node = WheelOdometryNode()             
    try:
        rclpy.spin(node)                     
    finally:
        rclpy.shutdown()                   

if __name__ == '__main__':
    main()