### NODE PURPOSE ###
"""
Using arrow keys to drive the robot from the terminal.
"""
### NODE PURPOSE ###


#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray, Bool

import sys
import tty
import termios
import threading


class TeleopNode(Node):
    def __init__(self):
        super().__init__('teleop_node')

        self.motor_driver_commands_publisher = self.create_publisher(
            Float32MultiArray,
            'motor_driver_commands',
            10
        )
        
        # depth camera obstruction alert
        self.depth_obstruction_alert_subscriber = self.create_subscription(
            Bool,
            'depth_obstruction_alert',
            self.process_obstruction_alert,
            10
        )
        
        self.depth_is_obstructed = False
        
        # Start the keyboard listener thread
        thread = threading.Thread(target=self.keyboard_listener)
        thread.daemon = True
        thread.start()

        self.get_logger().info("TELEOP NODE SUCCESSFULLY INITIATED")


    def process_obstruction_alert(self, msg):
        self.depth_is_obstructed = msg.data
            

    def getch(self):
        # Get the file descriptor for standard input (keyboard)
        fd = sys.stdin.fileno()

        # Save the current terminal settings so we can restore them later
        old_settings = termios.tcgetattr(fd)

        try:
            # Set the terminal to raw mode (no line buffering, no echo, etc.)
            tty.setraw(sys.stdin.fileno())

            # Read the first character from stdin
            ch1 = sys.stdin.read(1)

            # If the first character is an escape character, it could be an arrow key
            if ch1 == '\x1b':
                # Read the next two characters to complete the escape sequence
                ch2 = sys.stdin.read(1)
                ch3 = sys.stdin.read(1)
                # Return the full escape sequence (e.g., '\x1b[A' for up arrow)
                return ch1 + ch2 + ch3
            else:
                # Otherwise, return the single character (e.g., 'q')
                return ch1

        finally:
            # Restore the terminal to its original settings
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


    def publish_command(self, left, right, head_h, head_v, label):
        msg = Float32MultiArray()
        msg.data = [left, right, head_h, head_v]
        self.motor_driver_commands_publisher.publish(msg)
        self.get_logger().info(f"Published: {label}")


    def keyboard_listener(self):
        while True:
            key = self.getch()
            
            if key == '\x1b[A':  # up arrow
                if not self.depth_is_obstructed:
                    self.publish_command(200.0, 200.0, 90.0, 90.0, "FORWARD")
            elif key == '\x1b[B':  # down arrow
                self.publish_command(-200.0, -200.0, 90.0, 90.0, "BACKWARD")
            elif key == '\x1b[C':  # right arrow
                if not self.depth_is_obstructed:
                    self.publish_command(200.0, -200.0, 90.0, 90.0, "RIGHT")
            elif key == '\x1b[D':  # left arrow
                if not self.depth_is_obstructed:
                    self.publish_command(-200.0, 200.0, 90.0, 90.0, "LEFT")
            elif key == ' ':
                self.publish_command(0.0, 0.0, 90.0, 90.0, "STOP")
            elif key == 'q':
                self.get_logger().info("Quit command received")
                break


def main(args=None):
    rclpy.init(args=args)
    node = TeleopNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()