### NODE PURPOSE ###
"""
central processing node for the robot
"""
### NODE PURPOSE ###

#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from std_msgs.msg import Int16, String, Bool

# custom services and messages
from custom_interfaces.srv import ChangeFaceState, SetCustomNavigationGoal
from custom_interfaces.msg import DetectedPersonFrameOffset, IMUData, DetectedVoiceCommand, MoveRobotCommand, CustomNavigationGoal
from nav_msgs.msg import Odometry

import time
import math
import random


class CentralProcessingNode(Node): 
    def __init__(self):
        super().__init__("central_processing_node")
        
        #################
        ### VARIABLES ###
        #################
        
        self.robot_state = "TRACKING"
        self.current_head_state = "head_straight"
        
        self.robot_states = [
            "DEFAULT",
            "AUTONAV",
            "COMPANION",
            "TRACKING",
            "SECURITY",
            "REMOTE"
        ]
        
        
        ### VERIFY SUCCESSFUL INIT VARIABLES ###
        self.init_complete = False
        
        self.audio_direction_init = False
        self.imu_init = False
        self.odometry_init = False
        self.costmap_initiated = False
        
        ### MAIN VARIABLES ###
        self.current_audio_direction = 0
        
        self.person_x_offset = 0.0
        self.person_y_offset = 0.0
        
        self.accelerometer_x = 0.0
        self.accelerometer_y = 0.0
        self.accelerometer_z = 0.0
        self.gyroscope_x = 0.0
        self.gyroscope_y = 0.0
        self.gyroscope_z = 0.0
        
        self.latest_voice_cmd = ""
        self.latest_voice_cmd_direction = 0.0
        
        # odometry positional values
        self.current_robot_x = 0.0
        self.current_robot_y = 0.0
        self.current_robot_yaw = 0.0
        
        # random moves and cutenesss
        current_time = time.time()
        
        ### DEFAULT ###
        self.last_random_head_time = current_time
        self.next_head_interval = random.uniform(5.0, 40.0)

        self.last_random_face_time = current_time
        self.next_face_interval = random.uniform(5.0, 20.0)
        ### DEFAULT ###
        
        ### AUTO NAV ###
        self.last_random_goal_time = time.time()
        self.random_goal_interval = 15 # seconds
        ### AUTO NAV ###     
        
        ### TRACKING ###
        self.person_detection_computed = True
        ### TRACKING ###
             
        ### SECURITY ###   
        self.last_time_looking_at_person = current_time
        ### SECURITY ###

        ### MAIN ROBOT LOOP ###
        self.main_robot_timer = None
        ### MAIN ROBOT LOOP ###
        
        
        ###################
        ### SUBSCRIBERS ###
        ###################
        
        # audio direction
        self.audio_direction_subscriber = self.create_subscription(
            Int16,
            'audio_direction',
            self.process_audio_direction,
            10
        )
        
        # detected person frame offset
        self.detected_person_frame_offset_subscriber = self.create_subscription(
            DetectedPersonFrameOffset,
            'detected_person_frame_offset',
            self.process_person_frame_offset,
            10
        )
        
        # imu data
        self.imu_data_subscriber = self.create_subscription(
            IMUData,
            'imu_data',
            self.process_imu_data,
            10
        )
        
        # detected voice commands
        self.voice_commands_subscriber = self.create_subscription(
            DetectedVoiceCommand,
            'detected_voice_commands',
            self.process_voice_commands,
            10
        )
        
        # subscriber for odometry
        self.odom_subscriber = self.create_subscription(
            Odometry,
            '/odometry/filtered',
            self.update_odometry,
            10
        )
        
        self.costmap_initiated_subscriber = self.create_subscription(
            Bool,
            'costmap_initiated',
            self.set_costmap_success,
            10
        )
        
        
        ##################
        ### PUBLISHERS ###
        ##################
        
        # audio playback commands
        self.audio_commands_publisher = self.create_publisher(
            String, 
            'audio_playback_commands', 
            10
        )
        
        # light ring commands
        self.light_ring_commands_publisher = self.create_publisher(
            String, 
            'light_ring_commands', 
            10
        )
        
        # moving robot commands
        self.move_robot_commands_publisher = self.create_publisher(
            MoveRobotCommand, 
            'move_robot_command', 
            10
        )
        
        
        #######################
        ### SERVICE CLIENTS ###
        #######################
        
        # service clients
        self.change_face_state_client = self.create_client(ChangeFaceState, "change_face_state")
        self.custom_nav_goal_client = self.create_client(SetCustomNavigationGoal, "set_custom_navigation_goal")

        # waiting for services 
        self.change_face_state_client.wait_for_service()
        self.custom_nav_goal_client.wait_for_service()
        
        ### MAIN INIT ###
        self.verify_init_timer = self.create_timer(0.1, self.check_for_init)
        ### MAIN INIT ###
        
        self.get_logger().info("CENTRAL PROCESSING NODE SUCCESSFULLY INITIATED")
        
        
    #####################
    ### INIT FUNCTION ###
    #####################
    
    def check_for_init(self):        
        if all([self.audio_direction_init, self.imu_init, self.odometry_init, self.costmap_initiated]):
            self.verify_init_timer.cancel()
            
            # send init_procedure_complete to face_animation_node
            request = ChangeFaceState.Request()
            request.face_state = "init_procedure_complete"
            self.change_face_state_client.call_async(request)

            move_robot_command = MoveRobotCommand()
            move_robot_command.command = "init_move"
            move_robot_command.goal_angle = 0.0
            self.move_robot_commands_publisher.publish(move_robot_command)
                
            for _ in range(3):
                light_ring_cmd = String()
                light_ring_cmd.data = "flash_light_ring"
                self.light_ring_commands_publisher.publish(light_ring_cmd)
                time.sleep(0.8)

            # enabling main robot function
            self.init_complete = True
            self.main_robot_timer = self.create_timer(0.1, self.main_robot_function)
            
            self.get_logger().info("INIT PROCEDURE COMPLETE!")
            
            
    ###########################
    ### MAIN ROBOT FUNCTION ###
    ###########################
    
    def main_robot_function(self):
        
        ### STATE: DEFAULT ###
        if self.robot_state == "DEFAULT":
            current_time = time.time()

            if self.latest_voice_cmd == "kd-1":
                self.last_time_looking_at_person = current_time
                self.latest_voice_cmd = ""

                # --- HEAD OFFSET MAPPING (degrees) ---
                head_offsets = {
                    "head_left": 315.0,         # 360 - 45
                    "head_half_left": 337.5,    # 360 - 22.5
                    "head_straight": 0.0,
                    "head_half_right": 22.5,
                    "head_right": 45.0,
                }

                head_yaw_offset = head_offsets.get(self.current_head_state, 0.0)

                # --- Correct direction for head rotation ---
                corrected_direction = (self.latest_voice_cmd_direction - head_yaw_offset) % 360

                # --- Decision logic (in robot body frame) ---
                if corrected_direction <= 20 or corrected_direction >= 340:
                    # Voice is in front
                    self.kd1_attention()
                    self.current_head_state = "head_straight"
                    msg = MoveRobotCommand(command="head_straight", goal_angle=90.0)
                    self.move_robot_commands_publisher.publish(msg)

                elif 20 < corrected_direction < 60:
                    # Slightly to left
                    self.kd1_attention()
                    self.current_head_state = "head_half_left"
                    msg = MoveRobotCommand(command="head_half_left", goal_angle=90.0)
                    self.move_robot_commands_publisher.publish(msg)

                elif 60 <= corrected_direction < 100:
                    # Fully to left
                    self.kd1_attention()
                    self.current_head_state = "head_left"
                    msg = MoveRobotCommand(command="head_left", goal_angle=90.0)
                    self.move_robot_commands_publisher.publish(msg)

                elif 260 <= corrected_direction < 300:
                    # Fully to right
                    self.kd1_attention()
                    self.current_head_state = "head_right"
                    msg = MoveRobotCommand(command="head_right", goal_angle=90.0)
                    self.move_robot_commands_publisher.publish(msg)

                elif 300 <= corrected_direction < 340:
                    # Slightly to right
                    self.kd1_attention()
                    self.current_head_state = "head_half_right"
                    msg = MoveRobotCommand(command="head_half_right", goal_angle=90.0)
                    self.move_robot_commands_publisher.publish(msg)

                else:
                    # Sound is behind or unclear
                    self.kd1_attention("no")
                    self.current_head_state = "head_straight"
                    msg = MoveRobotCommand(command="shake_head", goal_angle=90.0)
                    self.move_robot_commands_publisher.publish(msg)
                    
            # random behavior
            elif current_time - self.last_time_looking_at_person > 10:                
                # random head move every 10 seconds
                if current_time - self.last_random_head_time > self.next_head_interval:
                    head_commands = ['shake_head', 'head_right', 'head_left', 'head_straight', 'head_half_left', 'head_half_right']
                    cmd = random.choice(head_commands)
                    
                    self.current_head_state = cmd

                    msg = MoveRobotCommand()
                    msg.command = cmd
                    msg.goal_angle = 90.0
                    self.move_robot_commands_publisher.publish(msg)
                    
                    self.last_random_head_time = current_time
                    self.next_head_interval = random.uniform(5.0, 40.0) 
                
                # random face look every 5 seconds
                if current_time - self.last_random_face_time > self.next_face_interval:
                    # favoring smile
                    face_commands = ['smile', 'smile', 'blink', 'blink', 'look_left', 'look_right', 'bored', 'sleep']
                    cmd = random.choice(face_commands)

                    req = ChangeFaceState.Request()
                    req.face_state = cmd

                    self.change_face_state_client.call_async(req)
                    
                    self.last_random_face_time = current_time
                    self.next_face_interval = random.uniform(5.0, 20.0)


        ### STATE: AUTONAV ###
        if self.robot_state == "AUTONAV":
            now = time.time()
            
            if now - self.last_random_goal_time > self.random_goal_interval:
                # Generate a random goal within 2 m radius of current position
                radius = random.uniform(0.2, 2.0)
                angle = random.uniform(0, 2 * math.pi)

                goal_x = self.current_robot_x + radius * math.cos(angle)
                goal_y = self.current_robot_y + radius * math.sin(angle)

                # Create and send the service request
                req = SetCustomNavigationGoal.Request()
                req.x = goal_x
                req.y = goal_y
                req.yaw = 0.0

                future = self.custom_nav_goal_client.call_async(req)

                # Handle response when done
                def callback(fut):
                    try:
                        res = fut.result()
                        
                        if res.goal_accepted:
                            self.last_random_goal_time = now
                            self.get_logger().info("New random goal accepted by navigation node!")
                        else:
                            self.get_logger().warn("Random goal rejected by navigation node!")
                    except Exception as e:
                        self.get_logger().error(f"Failed to call service: {e}")

                future.add_done_callback(callback)
        
            
        ### STATE: COMPANION ###
        if self.robot_state == "COMPANION":
            pass
            
            
        ### STATE: TRACKING ###
        if self.robot_state == "TRACKING":
            if not self.person_detection_computed:
                # move head towards person
                offset = self.person_x_offset

                if offset > 50.0:
                    desired_state = "head_right"
                elif 20.0 <= offset <= 50.0:
                    desired_state = "head_half_right"
                elif -50.0 <= offset <= -20.0:
                    desired_state = "head_half_left"
                elif offset < -50.0:
                    desired_state = "head_left"
                else:
                    desired_state = "head_straight"

                # only publish if state changes
                if self.current_head_state != desired_state:
                    self.current_head_state = desired_state
                    msg = MoveRobotCommand(command=desired_state, goal_angle=90.0)
                    self.move_robot_commands_publisher.publish(msg)
                
                # move closer to person
                if self.person_x_offset > 1.5:
                    req = SetCustomNavigationGoal.Request()
                    req.x = self.person_x_offset
                    req.y = self.person_y_offset
                    req.yaw = 0.0

                    self.custom_nav_goal_client.call_async(req)
                    
                # reset
                self.person_detection_computed = True

            
        ### STATE: SECURITY ###
        if self.robot_state == "SECURITY":
            pass
            
            
        ### STATE: REMOTE ###
        if self.robot_state == "REMOTE":
            pass
        
        
    ############################
    ### SUBSCRIBER CALLBACKS ###
    ############################
    
    def process_audio_direction(self, msg):
        if not self.audio_direction_init:
            self.audio_direction_init = True

        self.current_audio_direction = msg.data
                
    
    ### FRAME OFFSET DATA MEANING ###
    # x > 0: person right from center (robot pov)
    # x < 0: person left from center (robot pov)
                        
    # y > 0: person further away from robot than center
    # y < 0: person closer to robot than center          
    def process_person_frame_offset(self, msg):
        self.person_x_offset = msg.x_offset
        self.person_y_offset = msg.y_offset
        
        self.person_detection_computed = False
    
    
    def process_imu_data(self, msg):
        if not self.imu_init:
            self.imu_init = True
            
        self.accelerometer_x = msg.accelerometer_x
        self.accelerometer_y = msg.accelerometer_y
        self.accelerometer_z = msg.accelerometer_z
        self.gyroscope_x = msg.gyroscope_x
        self.gyroscope_y = msg.gyroscope_y
        self.gyroscope_z = msg.gyroscope_z
              
    
    def process_voice_commands(self, msg):
        self.latest_voice_cmd = msg.command
        self.latest_voice_cmd_direction = msg.command_direction
        
    
    def update_odometry(self, msg):
        if not self.odometry_init:
            self.odometry_init = True
            
        self.current_robot_x = msg.pose.pose.position.x
        self.current_robot_y = msg.pose.pose.position.y

        quaternion = msg.pose.pose.orientation

        formula_left_result = 2 * (quaternion.w * quaternion.z + quaternion.x * quaternion.y)
        formula_right_result = 1 - 2 * (quaternion.y * quaternion.y + quaternion.z * quaternion.z)

        self.current_robot_yaw = math.atan2(formula_left_result, formula_right_result)
        
    
    def set_costmap_success(self, msg):
        self.costmap_initiated = msg.data
        
        
    ########################
    ### HELPER FUNCTIONS ###
    ########################

    # creating a goal that is directly ahead of the current robots position
    def get_goal_ahead(self, distance=0.3):
        x = self.current_robot_x + distance * math.cos(self.current_robot_yaw)
        y = self.current_robot_y + distance * math.sin(self.current_robot_yaw)
        return x, y
    

    def kd1_attention(self, sound="yes"):
        audio_msg = String()
        
        if sound == "yes":
            audio_msg.data = "ATTENTION"
        elif sound == "no":
            audio_msg.data = "OKAY"
        self.audio_commands_publisher.publish(audio_msg)
                
        face = "smile"
        req = ChangeFaceState.Request()
        req.face_state = face
        self.change_face_state_client.call_async(req)


def main(args=None):
    rclpy.init(args=args)
    node = CentralProcessingNode()
    
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()