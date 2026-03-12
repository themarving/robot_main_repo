#!/usr/bin/env python3
"""
Navigation Node with Smoothed A* Path Planning and Obstacle Reaction
-------------------------------------------------------------------
Purpose:
    Uses a rolling local costmap to plan and follow a path from the
    robots current position to a goal, dynamically reacting to obstacles.

Topics:
    Subscribed:
        • /local_costmap/costmap (nav_msgs/OccupancyGrid)
        • /odometry/filtered (nav_msgs/Odometry)
    Published:
        • /move_robot_command (custom_interfaces/MoveRobotCommand)
        • /custom_plan (nav_msgs/Path)
    Service:
        • SetCustomNavigationGoal (x, y, yaw)
"""

### CLEARING COSTMAPS ###
# ros2 service call /local_costmap/clear_entirely_local_costmap nav2_msgs/srv/ClearEntireCostmap
# ros2 service call /global_costmap/clear_entirely_global_costmap nav2_msgs/srv/ClearEntireCostmap
### CLEARING COSTMAPS ###

import rclpy
from rclpy.node import Node
from nav_msgs.msg import OccupancyGrid, Odometry, Path
from nav2_msgs.srv import ClearEntireCostmap
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Bool
import math, heapq

from custom_interfaces.msg import MoveRobotCommand
from custom_interfaces.srv import SetCustomNavigationGoal

# ros2 service call /set_custom_navigation_goal custom_interfaces/srv/SetCustomNavigationGoal "{x: 1.5, y: -0.3, yaw: 0.0}"


class NavigationNode(Node):
    def __init__(self):
        super().__init__('navigation_node')
        
        self.emergency_stop = False
        self.navigation_timeout = 20 # seconds
        self.navigation_start_time = None

        self.local_costmap = None
        self.path = []
        self.is_navigating = False

        self.goal_threshold = 0.18
        self.tolerated_yaw_offset = 0.3
        self.path_replan_interval = 3.0
        self.obstacle_threshold = 30 # costmap cell value

        self.current_robot_x = 0.0
        self.current_robot_y = 0.0
        self.current_robot_yaw = 0.0

        self.goal_x = None
        self.goal_y = None
        self.goal_yaw = None
        
        # local costmap subscriber
        self.local_costmap_subscriber = self.create_subscription(
            OccupancyGrid, 
            '/local_costmap/costmap', 
            self.local_costmap_callback, 
            10
        )

        
        # odometry subscriber
        self.odom_subscriber = self.create_subscription(
            Odometry,
            '/odometry/filtered',
            self.update_odometry,
            10
        )
        
        # emergency stop subscriber
        self.emergency_stop_subscriber = self.create_subscription(
            Bool,
            'execute_emergency_stop',
            self.update_emergency_stop,
            10
        )
        
        # moving robot commands publisher
        self.move_robot_commands_publisher = self.create_publisher(
            MoveRobotCommand, 
            'move_robot_command', 
            10
        )
        
        # visualizing the path publisher
        self.path_publisher = self.create_publisher(
            Path,
            '/custom_plan',
            10
        )
        
        # costmap init publisher
        self.local_costmap_initiated_publisher = self.create_publisher(
            Bool,
            'local_costmap_initiated',
            10
        )
        
        # CUSTOM NAV GOAL SERVICE
        self.goal_service = self.create_service(
            SetCustomNavigationGoal,
            '/set_custom_navigation_goal',
            self.goal_service_callback
        )
                
        self.local_costmap_initiated = False
        
        self.local_costmap_client = self.create_client(ClearEntireCostmap, '/local_costmap/clear_entirely_local_costmap')
        self.local_costmap_client.wait_for_service()
        
        self.navigation_timer = self.create_timer(0.1, self.navigate)
        self.reset_costmap_timer = self.create_timer(10.0, self.clear_local_costmap)
        self.last_plan_time = self.get_clock().now()

        self.get_logger().info("NAVIGATION NODE SUCCESSFULLY INITIATED!")


    ###################
    ### SUBSCRIBERS ###
    ###################
    
    def update_emergency_stop(self, msg):
        self.emergency_stop = msg.data
        # self.get_logger().info(f"EMERGENCY STOP RECEIVED STOPPING = {msg.data}")

    def local_costmap_callback(self, msg):
        # initiating local costmap for central processing node
        if not self.local_costmap_initiated:
            self.local_costmap_initiated = True
            costmap_init = Bool()
            costmap_init.data = True
            self.local_costmap_initiated_publisher.publish(costmap_init)
            
        self.local_costmap = msg
            

    def goal_service_callback(self, request, response):
        # Original requested goal
        goal_x = request.x
        goal_y = request.y

        # --- Simple clamping to ±2.5 meters ---
        max_range = 2.5
        goal_x = max(-max_range, min(goal_x, max_range))
        goal_y = max(-max_range, min(goal_y, max_range))

        self.goal_x = goal_x
        self.goal_y = goal_y
        self.goal_yaw = request.yaw

        self.get_logger().info(
            f"New goal received via service: x={self.goal_x:.2f}, y={self.goal_y:.2f}, yaw={self.goal_yaw:.2f}"
        )
        
        # ensuring local costmap is available
        if self.local_costmap is None:
            response.goal_accepted = False
            self.is_navigating = False
            self.path = []
            self.get_logger().warn("Navigation service rejected: local costmap not initialized!")
            return response

        # planning path with A*
        planning_success = self.plan_path()
        
        now = self.get_clock().now()

        if planning_success:
            self.last_plan_time = now
            self.navigation_start_time = now
            self.is_navigating = True
            response.goal_accepted = True
            self.get_logger().info("Navigation service accepted: path planned successfully, starting navigation.")
        else:
            self.is_navigating = False
            self.path = []
            response.goal_accepted = False
            self.get_logger().warn("Service rejected: A* planning failed - no valid path found!")

        return response


    # extracting robot's current position from odometry message 
    def update_odometry(self, msg):
        self.current_robot_x = msg.pose.pose.position.x
        self.current_robot_y = msg.pose.pose.position.y
        
        # extracting orientation quaternion (represents robot's rotation in 3D space) 
        quaternion = msg.pose.pose.orientation
        
        # converting quaternion to yaw (rotation around Z axis)
        # Formula is standard quaternion → Euler angle conversion:
        # yaw = atan2(2*(w*z + x*y), 1 - 2*(y² + z²))
        formula_left_result = 2 * (quaternion.w * quaternion.z + quaternion.x * quaternion.y)
        formula_right_result = 1 - 2 * (quaternion.y * quaternion.y + quaternion.z * quaternion.z)

        # computing yaw angle in radians (robot’s heading direction in the plane)
        self.current_robot_yaw = math.atan2(formula_left_result, formula_right_result)


    ##################        
    ### NAVIGATION ###
    ##################

    def navigate(self):
        if not self.emergency_stop:
            if not self.is_navigating or self.local_costmap is None:
                return
            
            now = self.get_clock().now()
            
            # stopping navigation after timeout
            if (now - self.navigation_start_time).nanoseconds / 1e9 > self.navigation_timeout:
                self.publish_robot_move_command("stop", 0.0)
                self.is_navigating = False
                self.path = []
                self.get_logger().warn("NAVIGATION TIMED OUT!")
                return 

            dist_to_goal = math.hypot(self.goal_x - self.current_robot_x, self.goal_y - self.current_robot_y)
        
            # stopping robot when goal is reached
            if dist_to_goal < self.goal_threshold:
                self.publish_robot_move_command("stop", 0.0)
                self.is_navigating = False
                self.path = []
                
                self.get_logger().info(
                    f"NAVIGATION GOAL REACHED! Current odometry -> "
                    f"x={self.current_robot_x:.2f}, y={self.current_robot_y:.2f}, yaw={self.current_robot_yaw:.2f}"
                )
                
                return

            # going straight to goal for very close goals (2 * goal_threshold)
            if dist_to_goal < 2 * self.goal_threshold:
                self.path = [(self.goal_x, self.goal_y)]
                self.last_plan_time = now
            
            # replanning path after a set interval (detecting dynamic obstacles)
            if (now - self.last_plan_time).nanoseconds / 1e9 > self.path_replan_interval:
                self.last_plan_time = now
                self.plan_path()

            # follow path if available
            if self.path:
                self.follow_path()
            else:
                self.publish_robot_move_command("stop", 0.0)
                self.is_navigating = False
                self.path = []
                self.get_logger().warn("No path received from path planner - aborting!")
        else:
            # TO-DO: RECOVERY BEHAVIOR
            self.publish_robot_move_command("stop", 0.0)


    ####################  
    ### PATH PLANNER ###
    ####################  

    def plan_path(self):
        if not self.local_costmap:
            return False

        costmap_width = self.local_costmap.info.width
        costmap_height = self.local_costmap.info.height
        
        starting_point_in_map_grid = self.world_to_grid(self.current_robot_x, self.current_robot_y)
        goal_point_in_map_grid = self.world_to_grid(self.goal_x, self.goal_y)

        # verifying that starting position is within current costmap bounds
        if not (0 <= starting_point_in_map_grid[0] < costmap_width and 0 <= starting_point_in_map_grid[1] < costmap_height):
            self.get_logger().error("Start position outside costmap bounds!")
            return False
        
        # verifying that goal position is within current costmap bounds
        if not (0 <= goal_point_in_map_grid[0] < costmap_width and 0 <= goal_point_in_map_grid[1] < costmap_height):
            self.get_logger().warn(
                f"Goal is outside local costmap bounds! "
                f"Goal coordinates: x={goal_point_in_map_grid[0]:.2f}, y={goal_point_in_map_grid[1]:.2f} | "
                f"Costmap size: width={self.local_costmap.info.width:.2f}, height={self.local_costmap.info.height:.2f}"
            )
            return False

        path_cells = self.astar_search(self.local_costmap, starting_point_in_map_grid, goal_point_in_map_grid)
        
        # cancel navigation when no valid path is found -> NO RECOVERY BEHAVIOR
        if not path_cells:
            self.publish_robot_move_command("stop", 0.0)
            self.path = []
            self.is_navigating = False
            self.get_logger().warn("No valid path found with A* - aborting!")
            return False

        # simplifying the just found path (less zig zag)
        simplified_path_cells = self.simplify_path(path_cells)
        
        # setting the path with world points converted from map grid points
        self.path = [self.grid_to_world(i, j, self.local_costmap) for i, j in simplified_path_cells]
        # self.get_logger().info(f"Path planned with {len(self.path)} points.")
        
        # logging each point of the path
        # self.get_logger().info("Path points (world coordinates):")
        
        # for idx, (x, y) in enumerate(self.path):
        #     self.get_logger().info(f"  Point {idx}: x={x:.3f}, y={y:.3f}")
            
        # publish the path for visualization in RViz
        self.publish_path_to_rviz(self.path)
            
        return True


    # A* search -> finding shortest path from start to goal
    def astar_search(self, costmap, starting_point, goal_point):
        costmap_width = costmap.info.width              
        costmap_height = costmap.info.height            
        costmap_data = costmap.data                     

        # Heuristic function: estimates cost (Euclidean distance) between two points
        def heuristic(a, b):
            return math.hypot(a[0] - b[0], a[1] - b[1])

        # Generator function that yields all valid neighboring cells around a node
        def neighbors(node):
            x, y = node
            
            # Check all 8 possible directions (4 cardinal + 4 diagonal)
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]:
                nx, ny = x + dx, y + dy
                
                # Check if neighbor is within map boundaries
                if 0 <= nx < costmap_width and 0 <= ny < costmap_height:
                    idx = ny * costmap_width + nx      # Convert (x, y) to 1D index for costmap_data
                    
                    # Only consider cell if it is below obstacle threshold (i.e., not an obstacle)
                    if 0 <= costmap_data[idx] < self.obstacle_threshold:
                        # 'yield' returns one valid neighbor at a time instead of building a full list in memory.
                        # It pauses here and resumes from this point when next() is called on the generator.
                        yield (nx, ny)

        # Priority queue (min-heap) for open set, storing (estimated_total_cost, node)
        open_set = []
        heapq.heappush(open_set, (0, starting_point))   # Start with initial node

        came_from = {}                                 # Keeps track of best previous node for each visited cell
        g_score = {starting_point: 0}                  # Actual cost from start to this cell

        # Main A* loop — runs until all nodes are explored or goal is reached
        while open_set:
            _, current = heapq.heappop(open_set)        # Get node with lowest estimated cost (f-score)
            
            # If goal reached, reconstruct path by backtracking
            if current == goal_point:
                path = [current]
                
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                    
                path.reverse()                          # Reverse to go from start to goal
                return path

            # Check each valid neighbor of the current cell
            for nb in neighbors(current):
                tentative_g = g_score[current] + heuristic(current, nb)  # Cost to reach this neighbor
                
                # If new path to neighbor is better, record it
                if nb not in g_score or tentative_g < g_score[nb]:
                    came_from[nb] = current
                    g_score[nb] = tentative_g
                    f = tentative_g + heuristic(nb, goal_point)  # f = g + h
                    heapq.heappush(open_set, (f, nb))            # Add to open set with priority

        return None  # No path found
    
    
    # simplifying the path found by A* to reduce zig zag and make the robot's movements cleaner
    def simplify_path(self, path_cells):
        if not path_cells:
            return []
        
        # Start the simplified path with the first cell (starting position)
        simplified = [path_cells[0]]
        
        # Loop through all remaining points in the path
        for pt in path_cells[1:]:
            prev = simplified[-1]                 # Get the last point added to the simplified list
            dx = pt[0] - prev[0]                  # Change in x between current and previous point
            dy = pt[1] - prev[1]                  # Change in y between current and previous point
            dist = math.hypot(dx, dy)             # Euclidean distance between them
            
            # If the distance between current point and last simplified point > 1 cell (1.0)
            # then add it to the simplified path.
            # This skips over small "zigzag" movements between very close cells.
            if dist > 1.0:  
                simplified.append(pt)
                
        # Ensure the goal point (last cell of the original path) is always included
        if simplified[-1] != path_cells[-1]:
            simplified.append(path_cells[-1]) 
            
        return simplified


    #####################  
    ### PATH FOLLOWER ###
    #####################  

    def follow_path(self):
        if not self.path:
            return

        # Skip waypoints that are very close to the robot
        while self.path:
            target_x, target_y = self.path[0]  # Look at the first waypoint in the path
            
            # Compute Euclidean distance from robot to target waypoint
            dist = math.hypot(target_x - self.current_robot_x, target_y - self.current_robot_y)
            
            # If waypoint is closer than 0.15 meters, remove it from the path
            # This prevents the robot from trying to “over-correct” on tiny movements
            if dist < 0.15:
                self.path.pop(0)  # Remove the first element (closest waypoint)
            else:
                break  # Stop removing when we find a waypoint far enough away

        # If we removed all waypoints (path is empty), return
        if not self.path:
            return

        # Get the next target waypoint to move toward
        target_x, target_y = self.path[0]
        
        dx = target_x - self.current_robot_x  # X distance to waypoint
        dy = target_y - self.current_robot_y  # Y distance to waypoint
        
        distance = math.hypot(dx, dy)         # Euclidean distance to waypoint

        # Check if there’s an obstacle between the robot and this waypoint
        if self.is_obstacle_ahead():
            self.publish_robot_move_command("stop", 0.0)  # Stop robot immediately
            self.plan_path()  # Trigger path replanning to avoid obstacle
            self.get_logger().info("Obstacle detected — stopping and replanning path!")
            return

        # Compute angle toward target waypoint
        target_angle = math.atan2(dy, dx)  # Desired heading to waypoint
        angle_diff = self.normalize_angle(target_angle - self.current_robot_yaw)  # How much robot must turn

        # For very short segments (<0.2 m), ignore small turns to avoid jitter
        if distance < 0.2:
            angle_diff = 0

        # Decide whether to turn or move forward
        if abs(angle_diff) > self.tolerated_yaw_offset:
            # Robot needs to turn
            cmd = "turn_left" if angle_diff > 0 else "turn_right"
            self.publish_robot_move_command(cmd, abs(math.degrees(angle_diff)))  # Turn by required angle
        else:
            # Robot is roughly aligned — move forward slowly
            self.publish_robot_move_command("forwards_slow", 0.0)


    ########################  
    ### OBSTACLE CHECKER ###
    ########################  
    
    def is_obstacle_ahead(self):
        """
        Check a 30x30cm box that is 30cm ahead of the robot in the local costmap.
        Returns True if any cell in that box exceeds the obstacle threshold.
        """

        # Return False if the local costmap is not initialized yet
        if not self.local_costmap:
            return False

        # Box dimensions in meters
        box_width = 0.3
        box_length = 0.3
        box_offset = 0.3  # distance ahead of robot

        # Convert dimensions and offset to number of cells
        resolution = self.local_costmap.info.resolution        # meters per cell
        width_cells = int(box_width / resolution / 2)          # half-width
        length_cells = int(box_length / resolution)           # forward length
        offset_cells = int(box_offset / resolution)           # cells ahead of robot

        # Costmap size
        w = self.local_costmap.info.width
        h = self.local_costmap.info.height

        # Robot is always at the center of the rolling costmap
        cx = w // 2
        cy = h // 2

        # Loop through all cells in the rectangular box in front of the robot
        for li in range(offset_cells, offset_cells + length_cells):
            for wi in range(-width_cells, width_cells + 1):
                i = cx + li  # forward x index
                j = cy + wi  # sideways y index

                # # Skip out-of-bounds cells
                # if not (0 <= i < w and 0 <= j < h):
                #     continue

                # Convert 2D indices to 1D index
                idx = j * w + i

                # Return True immediately if obstacle detected
                if self.local_costmap.data[idx] >= self.obstacle_threshold:
                    return True

        # No obstacles detected in the checked area
        return False


    #################  
    ### UTILITIES ###
    #################  
    
    # converting map grid points to real world points (in meters - odometry position points)
    def grid_to_world(self, i, j, costmap):
        costmap_resolution = costmap.info.resolution
        origin_x = costmap.info.origin.position.x
        origin_y = costmap.info.origin.position.y
        
        x = origin_x + (i + 0.5) * costmap_resolution
        y = origin_y + (j + 0.5) * costmap_resolution
        
        return (x, y)
    
    
    # converting a position in world coordinates (meters, from odometry) 
    # to grid indices (i, j) in the local costmap
    def world_to_grid(self, x, y):
        if not self.local_costmap:
            return None
        
        costmap_resolution = self.local_costmap.info.resolution
        origin_x = self.local_costmap.info.origin.position.x
        origin_y = self.local_costmap.info.origin.position.y
        
        i = int((x - origin_x) / costmap_resolution)
        j = int((y - origin_y) / costmap_resolution)

        return i, j
    
    
    # keeping angle within bounds of -180 to 180 degrees
    def normalize_angle(self, angle):
        while angle > math.pi:
            angle -= 2 * math.pi
            
        while angle < -math.pi:
            angle += 2 * math.pi
            
        return angle
    

    def publish_robot_move_command(self, command, goal_angle):
        msg = MoveRobotCommand()
        msg.command = command
        msg.goal_angle = goal_angle
        self.move_robot_commands_publisher.publish(msg)
        

    # publish the computed A* path as a nav_msgs/Path
    def publish_path_to_rviz(self, path):
        if not path:
            return

        path_msg = Path()
        path_msg.header.stamp = self.get_clock().now().to_msg()
        path_msg.header.frame_id = "odom" # world reference frame in rviz

        for (x, y) in path:
            pose = PoseStamped()
            pose.header = path_msg.header
            pose.pose.position.x = x
            pose.pose.position.y = y
            pose.pose.orientation.w = 1.0  # Facing forward, no rotation
            path_msg.poses.append(pose)

        self.path_publisher.publish(path_msg)
        
        
    # local costmap clearing
    def clear_local_costmap(self):
        if not self.is_navigating:
            request = ClearEntireCostmap.Request()
            self.local_costmap_client.call_async(request)


def main(args=None):
    rclpy.init(args=args)
    node = NavigationNode()
    try:
        rclpy.spin(node)
    finally:
        rclpy.shutdown()


if __name__ == '__main__':
    main()