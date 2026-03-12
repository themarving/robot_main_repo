### NODE PURPOSE ###
"""
central processing node for the robot
"""
### NODE PURPOSE ###


#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from std_msgs.msg import Int16, String, Bool
from nav_msgs.msg import Odometry

# custom services and messages
from custom_interfaces.srv import ChangeFaceState
from custom_interfaces.msg import DetectedPersonFrameOffset, IMUData, DetectedVoiceCommand, MoveRobotCommand

import time


class CentralProcessingNode(Node): 
    def __init__(self):
        super().__init__("central_processing_node")
        
        #################
        ### VARIABLES ###
        #################
        
        ### VERIFY SUCCESSFUL INIT VARIABLES ###
        self.init_complete = False
        
        self.audio_direction_init = False
        self.depth_obstruction_init = False
        self.imu_init = False
        
        ### MAIN INIT ###
        self.verify_init_timer = self.create_timer(0.1, self.check_for_init)
        ### MAIN INIT ###
        
        ### MAIN VARIABLES ###
        self.current_audio_direction = 0
        self.depth_is_obstructed = True
        self.tof_is_obstructed = True
        
        self.person_x_offset = 0.0
        self.person_y_offset = 0.0
        self.last_time_person_detected = self.get_clock().now()
        
        self.accelerometer_x = 0.0
        self.accelerometer_y = 0.0
        self.accelerometer_z = 0.0
        self.gyroscope_x = 0.0
        self.gyroscope_y = 0.0
        self.gyroscope_z = 0.0
        
        self.latest_voice_cmd = ""
        self.latest_voice_cmd_direction = 0.0
        
        ### ODOMETRY ###
        self.odom_is_moving = False
        
        self.motion_start_time = None
        self.odom_check_delay_sec = 2.0
        
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
        
        # depth camera obstruction alert
        self.depth_obstruction_alert_subscriber = self.create_subscription(
            Bool,
            'depth_obstruction_alert',
            self.process_obstruction_alert,
            10
        )
        
        # tof sensor collision alert
        self.tof_sensors_alert_subscriber = self.create_subscription(
            Bool,
            'tof_sensors_alert',
            self.process_tof_sensors_alert,
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
        
        # using odom to detect collisions
        self.odom_subscriber = self.create_subscription(
            Odometry,
            '/odometry/filtered',
            self.update_odom_movement_status,
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
        
        # change face state client
        self.change_face_state_client = self.create_client(ChangeFaceState, "change_face_state")
        
        
        self.get_logger().info("CENTRAL PROCESSING NODE SUCCESSFULLY INITIATED")
        
        
    #####################
    ### INIT FUNCTION ###
    #####################
    
    def check_for_init(self):        
        if all([self.audio_direction_init, self.depth_obstruction_init, self.imu_init]):
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
        # # turning robot towards user
        # if self.latest_voice_cmd == "look at me":    
        #     voice_direction_angle = self.latest_voice_cmd_direction
            
        #     # self.get_logger().info("CMD ANGLE RECEIVED: " + str(voice_direction_angle))
            
        #     if voice_direction_angle <= 180:
        #         move_robot_command = MoveRobotCommand()
        #         move_robot_command.command = "turn_left"
        #         move_robot_command.goal_angle = float(voice_direction_angle)
        #         self.move_robot_commands_publisher.publish(move_robot_command)
        #     else: 
        #         move_robot_command = MoveRobotCommand()
        #         move_robot_command.command = "turn_right"
        #         move_robot_command.goal_angle = float(360 - voice_direction_angle)
        #         self.move_robot_commands_publisher.publish(move_robot_command)
            
        #     self.latest_voice_cmd = ""
      
        # elif self.latest_voice_cmd == "stop":  
        #     move_robot_command = MoveRobotCommand()
        #     move_robot_command.command = "stop"
        #     move_robot_command.goal_angle = 0.0
        #     self.move_robot_commands_publisher.publish(move_robot_command)
            
        #     self.latest_voice_cmd = ""
            
        #     self.get_logger().info("STOP RECEIVED")
            
        # elif self.latest_voice_cmd == "back":   
        #     move_robot_command = MoveRobotCommand()
        #     move_robot_command.command = "backwards_slow"
        #     move_robot_command.goal_angle = 0.0
        #     self.move_robot_commands_publisher.publish(move_robot_command)
            
        #     self.latest_voice_cmd = ""
            
        #     self.get_logger().info("BACK RECEIVED")
            
        # elif self.latest_voice_cmd == "move" and not self.depth_is_obstructed:   
        #     move_robot_command = MoveRobotCommand()
        #     move_robot_command.command = "forwards_slow"
        #     move_robot_command.goal_angle = 0.0
        #     self.move_robot_commands_publisher.publish(move_robot_command)
            
        #     self.latest_voice_cmd = ""
            
        #     self.get_logger().info("GO RECEIVED")
               
        # elif self.latest_voice_cmd == "left":  
        #     move_robot_command = MoveRobotCommand()
        #     move_robot_command.command = "turn_left"
        #     move_robot_command.goal_angle = 90.0
        #     self.move_robot_commands_publisher.publish(move_robot_command)
            
        #     self.latest_voice_cmd = ""
            
        #     self.get_logger().info("LEFT RECEIVED")
                
        # elif self.latest_voice_cmd == "right":   
        #     move_robot_command = MoveRobotCommand()
        #     move_robot_command.command = "turn_right"
        #     move_robot_command.goal_angle = 90.0
        #     self.move_robot_commands_publisher.publish(move_robot_command)  
            
        #     self.latest_voice_cmd = ""
            
        #     self.get_logger().info("RIGHT RECEIVED")
        pass

        
    ############################
    ### SUBSCRIBER CALLBACKS ###
    ############################
    
    def process_audio_direction(self, msg):
        if not self.init_complete and not self.audio_direction_init:
            self.get_logger().info("AUDIO DIRECTION INIT SUCCESSFUL")
            self.audio_direction_init = True
            self.current_audio_direction = msg.data
        else:
            self.current_audio_direction = msg.data
            
    
    def process_obstruction_alert(self, msg):
        if not self.init_complete and not self.depth_obstruction_init:
            self.get_logger().info("OBSTRUCTION ALERT INIT SUCCESSFUL")
            self.depth_obstruction_init = True
            self.depth_is_obstructed = msg.data
            
            if self.depth_is_obstructed:
                light_ring_cmd = String()
                light_ring_cmd.data = "path_obstructed"
                self.light_ring_commands_publisher.publish(light_ring_cmd)
            else:
                light_ring_cmd = String()
                light_ring_cmd.data = "obstruction_cleared"
                self.light_ring_commands_publisher.publish(light_ring_cmd)
                
        else: 
            self.depth_is_obstructed = msg.data
            
            if self.depth_is_obstructed:
                light_ring_cmd = String()
                light_ring_cmd.data = "path_obstructed"
                self.light_ring_commands_publisher.publish(light_ring_cmd)
            else:
                light_ring_cmd = String()
                light_ring_cmd.data = "obstruction_cleared"
                self.light_ring_commands_publisher.publish(light_ring_cmd)
                
                
    def process_tof_sensors_alert(self, msg):
        self.tof_is_obstructed = msg.data
            
    
    def process_person_frame_offset(self, msg):
        self.person_x_offset = msg.x_offset
        self.person_y_offset = msg.y_offset
        
        # updating timestamp for latest received message
        self.last_time_person_detected = self.get_clock().now()
    
    
    def process_imu_data(self, msg):
        if not self.init_complete and not self.imu_init:
            self.get_logger().info("IMU INIT SUCCESSFUL")
            self.imu_init = True
            
            self.accelerometer_x = msg.accelerometer_x
            self.accelerometer_y = msg.accelerometer_y
            self.accelerometer_z = msg.accelerometer_z
            self.gyroscope_x = msg.gyroscope_x
            self.gyroscope_y = msg.gyroscope_y
            self.gyroscope_z = msg.gyroscope_z
        else:
            self.accelerometer_x = msg.accelerometer_x
            self.accelerometer_y = msg.accelerometer_y
            self.accelerometer_z = msg.accelerometer_z
            self.gyroscope_x = msg.gyroscope_x
            self.gyroscope_y = msg.gyroscope_y
            self.gyroscope_z = msg.gyroscope_z
              
            
    def process_voice_commands(self, msg):
        self.latest_voice_cmd = msg.command
        self.latest_voice_cmd_direction = msg.command_direction
        
        
    def update_odom_movement_status(self, msg):
        # threshold for detecting movement
        linear_velocity_threshold = 0.02  # m/s

        current_velocity = msg.twist.twist.linear.x
        self.odom_is_moving = abs(current_velocity) > linear_velocity_threshold


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