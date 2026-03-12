#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from nav_msgs.msg import OccupancyGrid
from sensor_msgs.msg import PointCloud2
import numpy as np
import sensor_msgs_py.point_cloud2 as pc2
import tf2_ros
import tf2_sensor_msgs.tf2_sensor_msgs
from rclpy.time import Time


class CustomCostmapNode(Node):
    def __init__(self):
        super().__init__('custom_costmap_node')

        # --- Costmap parameters ---
        self.resolution = 0.1         # 10x10 cm cells
        self.height_threshold = 0.1   # meters
        self.max_height = 1.0         # meters
        self.min_points_per_cell = 3  # points to mark cell as occupied

        # Fixed rolling map size in meters
        self.map_size_x = 10.0
        self.map_size_y = 10.0

        # Number of cells
        self.width_cells = int(self.map_size_x / self.resolution)
        self.height_cells = int(self.map_size_y / self.resolution)

        # Rolling map origin (will be updated per robot position in odom)
        self.origin_x = 0.0
        self.origin_y = 0.0
        self.origin_z = 0.0  # flat on ground

        # Publisher
        self.costmap_publisher = self.create_publisher(
            OccupancyGrid, 
            '/custom_costmap', 
            10
        )

        # Subscriber
        self.pc_subscriber = self.create_subscription(
            PointCloud2, 
            '/depth_cam_pointcloud', 
            self.point_cloud_callback, 
            10
        )

        # OccupancyGrid template
        self.costmap = OccupancyGrid()
        self.costmap.header.frame_id = 'odom'  # map is in odom frame

        # Flat orientation
        self.flat_quat = (0.0, 0.0, 0.0, 1.0)

        # TF2 buffer & listener
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)

        # --- TEMPORAL SMOOTHING ---
        self.last_occupied_time = np.zeros((self.height_cells, self.width_cells), dtype=float)
        self.occupancy_lifetime = 2.0  # seconds

        # Publish at 5 Hz
        self.create_timer(0.2, self.publish_costmap)

        self.get_logger().info("CUSTOM COSTMAP NODE SUCCESSFULLY INITIATED!")

    # -------------------------
    # Callback: updates grid data
    # -------------------------
    def point_cloud_callback(self, cloud_msg: PointCloud2):
        # Transform cloud to odom frame
        try:
            transform = self.tf_buffer.lookup_transform(
                'odom',                    # target frame
                cloud_msg.header.frame_id,  # source frame
                Time())
            cloud_msg = tf2_sensor_msgs.tf2_sensor_msgs.do_transform_cloud(cloud_msg, transform)
        except Exception as e:
            self.get_logger().warn(f"TF transform failed: {e}")
            return

        # Convert PointCloud2 to numpy array
        points_gen = pc2.read_points(cloud_msg, field_names=("x", "y", "z"), skip_nans=True)
        points_list = [[float(p[0]), float(p[1]), float(p[2])] for p in points_gen]

        if len(points_list) == 0:
            return

        pc = np.array(points_list, dtype=np.float32)

        # --- FILTER POINTS BY HEIGHT THRESHOLD AND MAX HEIGHT ---
        pc = pc[(pc[:, 2] > self.height_threshold) & (pc[:, 2] <= self.max_height)]
        if pc.shape[0] == 0:
            return

        # --- Get robot position in odom frame ---
        try:
            robot_tf = self.tf_buffer.lookup_transform(
                'odom', 'base_link', Time())
            robot_x = robot_tf.transform.translation.x
            robot_y = robot_tf.transform.translation.y
        except Exception as e:
            self.get_logger().warn(f"TF lookup for robot failed: {e}")
            return

        # --- Rolling map origin centered on robot ---
        self.origin_x = robot_x - self.map_size_x / 2
        self.origin_y = robot_y - self.map_size_y / 2

        # Convert points to grid indices relative to map origin
        x_idx = np.clip(((pc[:, 0] - self.origin_x) / self.resolution).astype(int), 0, self.width_cells - 1)
        y_idx = np.clip(((pc[:, 1] - self.origin_y) / self.resolution).astype(int), 0, self.height_cells - 1)

        # Count points per cell
        grid_counts = np.zeros((self.height_cells, self.width_cells), dtype=np.int32)
        for xi, yi in zip(x_idx, y_idx):
            grid_counts[yi, xi] += 1

        # Initialize occupancy grid
        grid = np.zeros((self.height_cells, self.width_cells), dtype=np.int8)

        # --- TEMPORAL SMOOTHING ---
        current_time = self.get_clock().now().nanoseconds / 1e9  # seconds
        occupied_mask = grid_counts >= self.min_points_per_cell
        self.last_occupied_time[occupied_mask] = current_time

        time_since_occupied = current_time - self.last_occupied_time
        grid[time_since_occupied <= self.occupancy_lifetime] = 100

        # Fill OccupancyGrid message
        self.costmap.info.width = self.width_cells
        self.costmap.info.height = self.height_cells
        self.costmap.info.resolution = self.resolution
        self.costmap.info.origin.position.x = self.origin_x
        self.costmap.info.origin.position.y = self.origin_y
        self.costmap.info.origin.position.z = self.origin_z
        self.costmap.info.origin.orientation.x = self.flat_quat[0]
        self.costmap.info.origin.orientation.y = self.flat_quat[1]
        self.costmap.info.origin.orientation.z = self.flat_quat[2]
        self.costmap.info.origin.orientation.w = self.flat_quat[3]

        self.costmap.data = grid.flatten(order='C').astype(int).tolist()
        self.costmap.header.stamp = self.get_clock().now().to_msg()

    # -------------------------
    # Timer callback: publishes latest costmap
    # -------------------------
    def publish_costmap(self):
        if len(self.costmap.data) > 0:
            self.costmap.header.stamp = self.get_clock().now().to_msg()
            self.costmap_publisher.publish(self.costmap)


def main(args=None):
    rclpy.init(args=args)
    node = CustomCostmapNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
