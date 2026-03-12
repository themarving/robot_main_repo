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
from std_msgs.msg import String
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
        self.voice_command_publisher = self.create_publisher(String, 'detected_voice_commands', 10)
        
        # loading english Vosk model
        vosk_model_path = "/home/name/kd1_ws/src/main_pkg_python/vosk-model-small-en-us-0.15"
        
        try:
            vosk_model = Model(vosk_model_path)
        except Exception as e:
            self.get_logger().error(f"Failed to load Vosk model: {e}")
            raise

        # creating vosk recognizer
        self.recognizer = KaldiRecognizer(vosk_model, RESPEAKER_RATE)

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
        
        # list of commands
        self.voice_commands = [
            "kd one", 
            "katie one", 
            "stop", 
            "turn around"
        ]
        
        self.get_logger().info("VOICE RECOGNITION NODE SUCCESSFULLY INITIATED")
    
    
    # detecting voice commands
    def detect_voice_command(self, data):
        if self.recognizer.AcceptWaveform(data):
            result = self.recognizer.Result()
            result_dict = json.loads(result)
            text = result_dict.get("text", "")
            
            # Check if any of the command keywords are in the recognized text
            for command in self.voice_commands:
                if command in text.lower():
                    detected_command = String()
                    detected_command.data = command  
                    self.voice_command_publisher.publish(detected_command)

                    # stopping after the first match to avoid publishing multiple commands
                    break 
                
    # processing incoming audio continuously
    def audio_processing_thread(self):
        while rclpy.ok():
            try:
                data = self.audioStream.read(CHUNK, exception_on_overflow=False)
                self.detect_voice_command(data)
            except Exception as e:
                self.get_logger().error(f"Error processing audio: {e}")
            
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