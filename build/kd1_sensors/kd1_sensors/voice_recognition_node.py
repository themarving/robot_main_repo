### NODE PURPOSE ###
"""
recognizing users voice commands and publishing them
"""
### NODE PURPOSE ###

# Channel 0: processed audio for ASR
# Channel 1: mic1 raw data
# Channel 2: mic2 raw data
# Channel 3: mic3 raw data
# Channel 4: mic4 raw data
# Channel 5: merged playback

#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from std_msgs.msg import Int16
from custom_interfaces.msg import DetectedVoiceCommand

import threading
import pyaudio
from vosk import Model, KaldiRecognizer
import json

# mic array audio settings
RESPEAKER_RATE = 16000
RESPEAKER_CHANNELS = 1  # using 1 out of 5 channels for recognition
RESPEAKER_WIDTH = 2
RESPEAKER_INDEX = 1  # refers to the input device id
CHUNK = 4096

class VoiceRecognitionNode(Node): 
    def __init__(self):
        super().__init__("voice_recognition_node")
        
        # creating publisher for recognized voice commands
        self.voice_command_publisher = self.create_publisher(
            DetectedVoiceCommand, 
            'detected_voice_commands', 
            10
        )
        
        # audio direction
        self.audio_direction_subscriber = self.create_subscription(
            Int16,
            'audio_direction',
            self.process_audio_direction,
            10
        )
        
        # storing audio direction
        self.current_audio_direction = 0
        
        # list of commands
        self.voice_commands = [
            "hey",
            "hello",
            "what's up",
            "stop",
            "look at me",
            "come",
            "go back",
            "go left",
            "go right"
        ]
        
        self.wake_commands = [
            "hey",
            "hello",
            "what's up"
        ]

        # loading english Vosk model
        vosk_model_path = "/home/name/kd1_ws/src/kd1_sensors/vosk-model-small-en-us-0.15"
        
        try:
            vosk_model = Model(vosk_model_path)
        except Exception as e:
            self.get_logger().error(f"Failed to load Vosk model: {e}")
            raise

        # creating vosk recognizer
        #self.recognizer = KaldiRecognizer(vosk_model, RESPEAKER_RATE)

        # CHANGE: create recognizer with restricted grammar for higher reliability
        self.recognizer = KaldiRecognizer(vosk_model, RESPEAKER_RATE, json.dumps(self.voice_commands))

        # init PyAudio
        self.p = pyaudio.PyAudio()

        # creating audio stream
        self.audioStream = self.p.open(
            rate = RESPEAKER_RATE,
            format = self.p.get_format_from_width(RESPEAKER_WIDTH),
            channels = RESPEAKER_CHANNELS,
            input = True,
            input_device_index = RESPEAKER_INDEX,
            frames_per_buffer = CHUNK,
        )
        
        # continuous audio processing
        self.audio_thread = threading.Thread(target=self.audio_processing_thread)
        self.audio_thread.start()
        
        self.get_logger().info("VOICE RECOGNITION NODE SUCCESSFULLY INITIATED")
        
    
    def process_audio_direction(self, msg):
        self.current_audio_direction = msg.data
    
    
    # detecting voice commands and publishing with detection direction
    def detect_voice_command(self, data):
        command_direction = self.current_audio_direction
        
        if self.recognizer.AcceptWaveform(data):
            result = self.recognizer.Result()
            result_dict = json.loads(result)
            text = result_dict.get("text", "")
            
            # self.get_logger().info(f"Vosk JSON Result: {json.dumps(result_dict, indent=2)}")
            
            # self.get_logger().info(f"I HEARD: {text}")

            for command in self.voice_commands:
                if command in text.lower():
                    detected_command = DetectedVoiceCommand()
                    
                    # all wake commands trigger kd-1
                    if command in self.wake_commands:
                        detected_command.command = "kd-1"
                        detected_command.command_direction = command_direction
                        self.voice_command_publisher.publish(detected_command)
                        break
                    
                    detected_command.command = command
                    detected_command.command_direction = command_direction
                    self.voice_command_publisher.publish(detected_command)                

                    break # stopping after the first match to avoid publishing multiple commands
                
                
    # processing incoming audio continuously
    def audio_processing_thread(self):
        while rclpy.ok():
            try:
                data = self.audioStream.read(CHUNK, exception_on_overflow=False)
                self.detect_voice_command(data)
                
            except Exception as e:
                pass
            
            # allowing ROS 2 to handle other callbacks if neccessary, so far none implemented
            rclpy.spin_once(self, timeout_sec=0.1)


def main(args=None):
    rclpy.init(args=args)
    node = VoiceRecognitionNode()
    
    try:
        rclpy.spin(node)
    finally:
        node.audioStream.stop_stream()
        node.audioStream.close()
        node.p.terminate()
        
         # stopping thread when the node is shut down
        node.audio_thread.join()
        
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()