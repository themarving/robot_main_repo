### NODE PURPOSE ###
"""
creating service to change the robots face and animating the idle face while service not called
"""
### NODE PURPOSE ###


#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

# custom change face state service
from custom_interfaces.srv import ChangeFaceState

# for rgb matrix
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image

# sprites
smile_file = "/home/name/kd1_ws/src/kd1_utility_nodes/image_resources/smile.png"
blink_file = "/home/name/kd1_ws/src/kd1_utility_nodes/image_resources/blink.png"
interim_blink_file = "/home/name/kd1_ws/src/kd1_utility_nodes/image_resources/interim_blink.png"
look_left_file = "/home/name/kd1_ws/src/kd1_utility_nodes/image_resources/look_left.png"
look_right_file = "/home/name/kd1_ws/src/kd1_utility_nodes/image_resources/look_right.png"
init_1_file = "/home/name/kd1_ws/src/kd1_utility_nodes/image_resources/init_1.png"
init_2_file = "/home/name/kd1_ws/src/kd1_utility_nodes/image_resources/init_2.png"
init_3_file = "/home/name/kd1_ws/src/kd1_utility_nodes/image_resources/init_3.png"
init_4_file = "/home/name/kd1_ws/src/kd1_utility_nodes/image_resources/init_4.png"

# ros2 service call /change_face_state custom_interfaces/srv/ChangeFaceState "{face_state: init_procedure_complete}" --once


class FaceAnimationNode(Node): 
    def __init__(self):
        super().__init__("face_animation_node")
        
        # configuration for the matrix
        self.options = RGBMatrixOptions()
        self.options.rows = 32
        self.options.cols = 64
        self.options.chain_length = 1
        self.options.parallel = 1
        self.options.hardware_mapping = 'adafruit-hat'
        
        self.rgb_matrix = RGBMatrix(options=self.options)
        
        # create image objects
        self.smile = Image.open(smile_file)
        self.blink = Image.open(blink_file)
        self.interim_blink = Image.open(interim_blink_file)
        self.look_left = Image.open(look_left_file)
        self.look_right = Image.open(look_right_file)
        
        self.init_1 = Image.open(init_1_file)
        self.init_2 = Image.open(init_2_file)
        self.init_3 = Image.open(init_3_file)
        self.init_4 = Image.open(init_4_file)
        
        # make image fit our screen
        self.smile.thumbnail((self.rgb_matrix.width, self.rgb_matrix.height), Image.ANTIALIAS)
        self.blink.thumbnail((self.rgb_matrix.width, self.rgb_matrix.height), Image.ANTIALIAS)
        self.interim_blink.thumbnail((self.rgb_matrix.width, self.rgb_matrix.height), Image.ANTIALIAS)
        self.look_left.thumbnail((self.rgb_matrix.width, self.rgb_matrix.height), Image.ANTIALIAS)
        self.look_right.thumbnail((self.rgb_matrix.width, self.rgb_matrix.height), Image.ANTIALIAS)
        
        self.init_1.thumbnail((self.rgb_matrix.width, self.rgb_matrix.height), Image.ANTIALIAS)
        self.init_2.thumbnail((self.rgb_matrix.width, self.rgb_matrix.height), Image.ANTIALIAS)
        self.init_3.thumbnail((self.rgb_matrix.width, self.rgb_matrix.height), Image.ANTIALIAS)
        self.init_4.thumbnail((self.rgb_matrix.width, self.rgb_matrix.height), Image.ANTIALIAS)

        # face STATES and corresponding images
        self.face_states = {
            "smile": self.smile,
            "blink": self.blink,
            "interim_blink": self.interim_blink,
            "look_left": self.look_left,
            "look_right": self.look_right,
            "init_1": self.init_1,
            "init_2": self.init_2,
            "init_3": self.init_3,
            "init_4": self.init_4,
        }
        
        # current state on init smile
        self.current_state = ""
        
        # only allowing idle animation while no external face state call is being made
        self.allow_animation = True
        self.init_procedure = True
        
        # creating SERVICE for changing face
        self.change_face_state_server = self.create_service(ChangeFaceState, "change_face_state", self.changeFaceStateService)
        
        # timer for init ANIMATION
        self.init_animation_step = 0
        self.init_animation_timer = self.create_timer(0.5, self.updateInitAnimation)
        
        # timer for idle ANIMATION
        self.idle_animation_step = 0
        self.idle_animation_timer = self.create_timer(4.0, self.updateIdleAnimation)

        self.get_logger().info("FACE ANIMATION NODE SUCCESSFULLY INITIATED")
    
    
    # changing face state SERVICE
    def changeFaceStateService(self, request, response):   
        # defaulting to false
        response.face_state_changed = False
        
        # disabling init procedure and allowing face state changes to be made
        if request.face_state == "init_procedure_complete":
            self.init_procedure = False
            self.init_animation_timer.cancel()
            
            self.current_state = "smile"
            self.updateMatrix(self.current_state)
            
            self.get_logger().info(f"init procedure successfully completed, switching to idle animation")
            
            response.face_state_changed = True
            return response
        
        # no face state change service during init procedure
        if self.init_procedure:
            self.get_logger().warning("init procedure! Face state change not permitted")
            return response
                     
        # if requested face state invalid
        if request.face_state not in self.face_states:
            self.get_logger().warning("invalid face state requested!")
            return response
        else:             
            if request.face_state == "smile":
                # enabling idle animation
                self.allow_animation = True
                self.current_state = request.face_state  
                self.updateMatrix(self.current_state)

                self.get_logger().info(f"Face state successfully changed to: {self.current_state}")
            else:  
                # disabling idle animation during external face state request            
                self.allow_animation = False
                self.current_state = request.face_state  
                self.updateMatrix(self.current_state)
            
                self.get_logger().info(f"Face state successfully changed to: {self.current_state}")
            
            response.face_state_changed = True
            return response

    # update the RGB matrix with the image corresponding to the current face state
    def updateMatrix(self, state):
        image_to_display = self.face_states.get(state) 
        self.rgb_matrix.SetImage(image_to_display.convert('RGB'))
        
    def updateInitAnimation(self):
        if self.init_procedure:
            if self.init_animation_step == 0:
                self.updateMatrix("init_1")
                self.init_animation_step = 1
            elif self.init_animation_step == 1:
                self.updateMatrix("init_2")
                self.init_animation_step = 2
            elif self.init_animation_step == 2:
                self.updateMatrix("init_3")
                self.init_animation_step = 3
            elif self.init_animation_step == 3:
                self.updateMatrix("init_4")
                self.init_animation_step = 4
            elif self.init_animation_step == 4:
                self.updateMatrix("init_3")
                self.init_animation_step = 5
            elif self.init_animation_step == 5:
                self.updateMatrix("init_2")
                self.init_animation_step = 0
        
    def updateIdleAnimation(self):
        if self.allow_animation and self.init_procedure == False:
            # update animation based on the step
            if self.idle_animation_step == 0:
                self.updateMatrix("smile")
                self.idle_animation_step = 1
                self.idle_animation_timer.cancel() 
                self.idle_animation_timer = self.create_timer(4.0, self.updateIdleAnimation) # 4 seconds
            elif self.idle_animation_step == 1:
                self.updateMatrix("interim_blink")
                self.idle_animation_step = 2
                self.idle_animation_timer.cancel()  
                self.idle_animation_timer = self.create_timer(0.02, self.updateIdleAnimation) # 0.02 seconds
            elif self.idle_animation_step == 2:
                self.updateMatrix("blink")
                self.idle_animation_step = 3
                self.idle_animation_timer.cancel()
                self.idle_animation_timer = self.create_timer(1.2, self.updateIdleAnimation) # 1.2 seconds
            elif self.idle_animation_step == 3:
                self.updateMatrix("interim_blink")
                self.idle_animation_step = 0
                self.idle_animation_timer.cancel() 
                self.idle_animation_timer = self.create_timer(0.03, self.updateIdleAnimation) # 0.03 seconds
        else:
            self.idle_animation_step = 0
        

def main(args=None):
    rclpy.init(args=args)
    node = FaceAnimationNode() 
    
    try:
        rclpy.spin(node)
    except:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()