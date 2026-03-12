### NODE PURPOSE ###
"""
playing audio files which are triggered through a subscriber 
"""
### NODE PURPOSE ###


#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

import pygame

# ros2 topic pub /audio_playback_commands std_msgs/msg/String "data: OKAY" --once


class AudioPlaybackNode(Node): 
    def __init__(self):
        super().__init__("audio_playback_node")
        
        # initialize the mixer module
        pygame.mixer.init()
                
        # mapping commands to audio file paths
        self.audio_files = {
            'OKAY': '/home/name/kd1_ws/src/kd1_utility_nodes/audio_resources/kd1_okay.wav',
            'CONFIRM': '/home/name/kd1_ws/src/kd1_utility_nodes/audio_resources/kd1_confirm.wav',
            'ATTENTION': '/home/name/kd1_ws/src/kd1_utility_nodes/audio_resources/kd1_attention.wav',
            'ALERT': '/home/name/kd1_ws/src/kd1_utility_nodes/audio_resources/kd1_alert.wav',
        }
        
        # subscriber to receive audio playback commands
        self.audio_playback_subscriber = self.create_subscription(
            String,
            'audio_playback_commands',
            self.process_command,
            10
        )
        
        self.get_logger().info("AUDIO PLAYBACK NODE SUCCESSFULLY INITIATED")
        
    
    def process_command(self, msg):
        command = msg.data
        
        if command in self.audio_files:
            audio_path = self.audio_files[command]
            
            try:
                # load and play the selected audio file
                pygame.mixer.music.load(audio_path)
                pygame.mixer.music.play()
                # self.get_logger().info(f"Successfully played audio command: {command}")
            except Exception as e:
                self.get_logger().error(f"Failed to play audio file: {audio_path}. Error: {str(e)}")


def main(args=None):
    rclpy.init(args=args)
    node = AudioPlaybackNode()
    
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()