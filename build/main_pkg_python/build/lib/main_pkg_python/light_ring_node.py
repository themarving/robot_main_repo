### NODE PURPOSE ###
"""
creating a subscriber for letting the led ring be controlled
"""
### NODE PURPOSE ###


#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from pixel_ring import pixel_ring
from std_msgs.msg import String
import time

# ros2 topic pub /light_ring_commands std_msgs/msg/String "data: flash_light_ring"
# ros2 topic pub /light_ring_commands std_msgs/msg/String "data: red_alert"


class LightRingNode(Node): 
    def __init__(self):
        super().__init__("light_ring_node")
        
        # turning lights off on boot up
        pixel_ring.off()    

        # custom color patterns
        self.cyan = self.cyan_pattern()
        self.red = self.red_pattern()       
        
        # subscriber to receive light ring commands
        self.subscription = self.create_subscription(
            String,
            'light_ring_commands',
            self.process_command,
            10
        )
        
        self.get_logger().info("LIGHT RING NODE SUCCESSFULLY INITIATED")


    ##############
    ### COLORS ###
    ##############
            
    def cyan_pattern(self):
        # list of custom colors for each of the 12 LEDs on the pixel ring
        colors = [
            [0, 0, 0, 0],   
            [0, 255, 255, 0], 
            [0, 0, 0, 0],   
            [0, 255, 255, 0], 
            [0, 0, 0, 0],  
            [0, 0, 0, 0],
            [0, 0, 0, 0],  
            [0, 255, 255, 0], 
            [0, 0, 0, 0],  
            [0, 255, 255, 0], 
            [0, 0, 0, 0], 
            [0, 0, 0, 0] 
        ]
        
        flat_colors = []

        # append each color to the list
        for led_color in colors:
            for color in led_color:
                flat_colors.append(color)

        return flat_colors
    
    def red_pattern(self):
        colors = [
            [0, 0, 0, 0],   
            [255, 0, 0, 0], 
            [0, 0, 0, 0],   
            [255, 0, 0, 0], 
            [0, 0, 0, 0],  
            [0, 0, 0, 0],
            [0, 0, 0, 0],  
            [255, 0, 0, 0], 
            [0, 0, 0, 0],  
            [255, 0, 0, 0], 
            [0, 0, 0, 0], 
            [0, 0, 0, 0] 
        ]
        
        flat_colors = []

        # append each color to the list
        for led_color in colors:
            for color in led_color:
                flat_colors.append(color)

        return flat_colors
    
    
    ################
    ### LIGHT FX ###
    ################
    
    def flash_light_ring_cyan(self):
        # flashing the lights twice within one second
        for _ in range(2):
            # turn lights on with the desired color
            pixel_ring.customize(self.cyan) 
            pixel_ring.set_brightness(10)   
                   
            time.sleep(0.1)                       
            pixel_ring.off()                       
            time.sleep(0.1)                       

        # ensuring lights remain off after the flashes
        pixel_ring.off()
        
    def flash_light_ring_red(self):
        # flashing the lights twice within one second
        for _ in range(2):
            # turn lights on with the desired color
            pixel_ring.customize(self.red) 
            pixel_ring.set_brightness(10)   
                   
            time.sleep(0.1)                       
            pixel_ring.off()                       
            time.sleep(0.1)                       

        # ensuring lights remain off after the flashes
        pixel_ring.off()
    
    
    #####################
    ### CMD EXECUTION ###
    #####################
    
    def process_command(self, msg):
        if msg.data == "flash_light_ring":
            self.flash_light_ring_cyan()
        elif msg.data == "red_alert":
            self.flash_light_ring_red()
        
        
def main(args=None):
    rclpy.init(args=args)
    node = LightRingNode() 
    
    try:
        rclpy.spin(node)
    finally:
        # ensure the pixel ring is turned off on shutdown
        pixel_ring.off()
        rclpy.shutdown()


if __name__ == "__main__":
    main()