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
look_left_blink_file = "/home/name/kd1_ws/src/kd1_utility_nodes/image_resources/look_left_blink.png"
look_left_blink_interim_file = "/home/name/kd1_ws/src/kd1_utility_nodes/image_resources/look_left_blink_interim.png"
look_right_file = "/home/name/kd1_ws/src/kd1_utility_nodes/image_resources/look_right.png"
look_right_blink_file = "/home/name/kd1_ws/src/kd1_utility_nodes/image_resources/look_right_blink.png"
look_right_blink_interim_file = "/home/name/kd1_ws/src/kd1_utility_nodes/image_resources/look_right_blink_interim.png"
init_1_file = "/home/name/kd1_ws/src/kd1_utility_nodes/image_resources/init_1.png"
init_2_file = "/home/name/kd1_ws/src/kd1_utility_nodes/image_resources/init_2.png"
init_3_file = "/home/name/kd1_ws/src/kd1_utility_nodes/image_resources/init_3.png"
init_4_file = "/home/name/kd1_ws/src/kd1_utility_nodes/image_resources/init_4.png"
bored_face_file = "/home/name/kd1_ws/src/kd1_utility_nodes/image_resources/bored_face.png"
alert_face_file = "/home/name/kd1_ws/src/kd1_utility_nodes/image_resources/alert_face.png"
strange_one_file = "/home/name/kd1_ws/src/kd1_utility_nodes/image_resources/strange_face_one.png"
strange_two_file = "/home/name/kd1_ws/src/kd1_utility_nodes/image_resources/strange_face_two.png"
sleep_face_file = "/home/name/kd1_ws/src/kd1_utility_nodes/image_resources/sleep_face.png"

# ros2 service call /change_face_state custom_interfaces/srv/ChangeFaceState "{face_state: init_procedure_complete}" 


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
        
        # Set brightness (0-100)
        self.options.brightness = 35  # 50% brightness
        
        self.rgb_matrix = RGBMatrix(options=self.options)
        
        # create image objects
        self.smile = Image.open(smile_file)
        self.blink = Image.open(blink_file)
        self.interim_blink = Image.open(interim_blink_file)
        self.look_left = Image.open(look_left_file)
        self.look_left_blink = Image.open(look_left_blink_file)
        self.look_left_blink_interim = Image.open(look_left_blink_interim_file)
        self.look_right = Image.open(look_right_file)
        self.look_right_blink = Image.open(look_right_blink_file)
        self.look_right_blink_interim = Image.open(look_right_blink_interim_file)
        
        self.bored = Image.open(bored_face_file)
        self.alert = Image.open(alert_face_file)
        self.strange_one = Image.open(strange_one_file)
        self.strange_two = Image.open(strange_two_file)
        self.sleep = Image.open(sleep_face_file)
        
        self.init_1 = Image.open(init_1_file)
        self.init_2 = Image.open(init_2_file)
        self.init_3 = Image.open(init_3_file)
        self.init_4 = Image.open(init_4_file)
        
        # make image fit our screen
        self.smile.thumbnail((self.rgb_matrix.width, self.rgb_matrix.height), Image.ANTIALIAS)
        self.blink.thumbnail((self.rgb_matrix.width, self.rgb_matrix.height), Image.ANTIALIAS)
        self.interim_blink.thumbnail((self.rgb_matrix.width, self.rgb_matrix.height), Image.ANTIALIAS)
        self.look_left.thumbnail((self.rgb_matrix.width, self.rgb_matrix.height), Image.ANTIALIAS)
        self.look_left_blink.thumbnail((self.rgb_matrix.width, self.rgb_matrix.height), Image.ANTIALIAS)
        self.look_left_blink_interim.thumbnail((self.rgb_matrix.width, self.rgb_matrix.height), Image.ANTIALIAS)
        self.look_right.thumbnail((self.rgb_matrix.width, self.rgb_matrix.height), Image.ANTIALIAS)
        self.look_right_blink.thumbnail((self.rgb_matrix.width, self.rgb_matrix.height), Image.ANTIALIAS)
        self.look_right_blink_interim.thumbnail((self.rgb_matrix.width, self.rgb_matrix.height), Image.ANTIALIAS)
           
        self.bored.thumbnail((self.rgb_matrix.width, self.rgb_matrix.height), Image.ANTIALIAS)
        self.alert.thumbnail((self.rgb_matrix.width, self.rgb_matrix.height), Image.ANTIALIAS)
        self.strange_one.thumbnail((self.rgb_matrix.width, self.rgb_matrix.height), Image.ANTIALIAS)
        self.strange_two.thumbnail((self.rgb_matrix.width, self.rgb_matrix.height), Image.ANTIALIAS)
        self.sleep.thumbnail((self.rgb_matrix.width, self.rgb_matrix.height), Image.ANTIALIAS)
        
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
            "look_left_blink": self.look_left_blink,
            "look_left_blink_interim": self.look_left_blink_interim,
            "look_right": self.look_right,
            "look_right_blink": self.look_right_blink,
            "look_right_blink_interim": self.look_right_blink_interim,
            "init_1": self.init_1,
            "init_2": self.init_2,
            "init_3": self.init_3,
            "init_4": self.init_4,
            "bored": self.bored,
            "alert": self.alert,
            "strange_one": self.strange_one,
            "strange_two": self.strange_two,
            "sleep": self.sleep,
        }
        
        # current state on init smile
        self.current_state = ""
        
        # only allowing idle animation while no external face state call is being made
        self.allow_smile_animation = False
        self.allow_look_left_animation = False
        self.allow_look_right_animation = False
        self.init_procedure = True
        
        # creating SERVICE for changing face
        self.change_face_state_server = self.create_service(ChangeFaceState, "change_face_state", self.changeFaceStateService)
        
        # timer for init ANIMATION
        self.init_animation_step = 0
        self.init_animation_timer = self.create_timer(0.5, self.updateInitAnimation)
        
        # timer for idle ANIMATION
        self.smile_animation_step = 0
        self.smile_animation_timer = self.create_timer(4.0, self.updateSmileAnimation)
        
        self.look_left_animation_step = 0
        self.look_left_animation_timer = self.create_timer(4.0, self.updateLookLeftAnimation)
        
        self.look_right_animation_step = 0
        self.look_right_animation_timer = self.create_timer(4.0, self.updateLookRightAnimation)

        self.get_logger().info("FACE ANIMATION NODE SUCCESSFULLY INITIATED")
    
    
    # changing face state SERVICE
    def changeFaceStateService(self, request, response):   
        # defaulting to false
        response.face_state_changed = False
        
        # disabling init procedure and allowing face state changes to be made
        if request.face_state == "init_procedure_complete" and self.init_procedure:
            self.init_procedure = False
            self.init_animation_timer.cancel()
            
            self.allow_smile_animation = True
            
            self.current_state = "smile"
            self.updateMatrix(self.current_state)
            
            response.face_state_changed = True
            return response
        
        # no face state change service during init procedure
        if self.init_procedure:
            self.get_logger().warn("init procedure! Face state change not permitted")
            return response
                     
        # if requested face state invalid
        if request.face_state not in self.face_states:
            self.get_logger().warn("invalid face state requested!")
            return response
        
        else:             
            if request.face_state == "smile":
                self.allow_smile_animation = True
                self.allow_look_left_animation = False
                self.allow_look_right_animation = False
                
                self.smile_animation_step = 1
                
                self.current_state = request.face_state  
                self.updateMatrix(self.current_state)

            elif request.face_state == "look_left":
                self.allow_smile_animation = False
                self.allow_look_left_animation = True
                self.allow_look_right_animation = False
                
                self.look_left_animation_step = 1
                
                self.current_state = request.face_state  
                self.updateMatrix(self.current_state)

            elif request.face_state == "look_right":
                self.allow_smile_animation = False
                self.allow_look_left_animation = False
                self.allow_look_right_animation = True
                
                self.look_right_animation_step = 1
            
                self.current_state = request.face_state  
                self.updateMatrix(self.current_state)
            
            else:  
                self.allow_smile_animation = False
                self.allow_look_left_animation = False
                self.allow_look_right_animation = False
                
                self.current_state = request.face_state  
                self.updateMatrix(self.current_state)
            
            response.face_state_changed = True
            return response

    # update the RGB matrix with the image corresponding to the current face state
    def updateMatrix(self, state):
        image_to_display = self.face_states.get(state) 
        self.rgb_matrix.SetImage(image_to_display.convert('RGB'))
        
    # INIT ANIMATION
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
        
    # SMILE ANIMATION
    def updateSmileAnimation(self):
        if self.allow_smile_animation and self.init_procedure == False:
            if self.smile_animation_step == 0:
                self.updateMatrix("smile")
                self.smile_animation_step = 1
                self.smile_animation_timer.cancel()
                self.smile_animation_timer = self.create_timer(4.0, self.updateSmileAnimation) # 4 seconds
            elif self.smile_animation_step == 1:
                self.updateMatrix("interim_blink")
                self.smile_animation_step = 2
                self.smile_animation_timer.cancel()  
                self.smile_animation_timer = self.create_timer(0.02, self.updateSmileAnimation) # 0.02 seconds
            elif self.smile_animation_step == 2:
                self.updateMatrix("blink")
                self.smile_animation_step = 3
                self.smile_animation_timer.cancel()
                self.smile_animation_timer = self.create_timer(1.2, self.updateSmileAnimation) # 1.2 seconds
            elif self.smile_animation_step == 3:
                self.updateMatrix("interim_blink")
                self.smile_animation_step = 0
                self.smile_animation_timer.cancel() 
                self.smile_animation_timer = self.create_timer(0.03, self.updateSmileAnimation) # 0.03 seconds
        else:
            self.smile_animation_step = 0
            
    # LOOK LEFT ANIMATION
    def updateLookLeftAnimation(self):
        if self.allow_look_left_animation and self.init_procedure == False:
            if self.look_left_animation_step == 0:
                self.updateMatrix("look_left")
                self.look_left_animation_step = 1
                self.look_left_animation_timer.cancel() 
                self.look_left_animation_timer = self.create_timer(4.0, self.updateLookLeftAnimation) # 4 seconds
            elif self.look_left_animation_step == 1:
                self.updateMatrix("look_left_blink_interim")
                self.look_left_animation_step = 2
                self.look_left_animation_timer.cancel()  
                self.look_left_animation_timer = self.create_timer(0.02, self.updateLookLeftAnimation) # 0.02 seconds
            elif self.look_left_animation_step == 2:
                self.updateMatrix("look_left_blink")
                self.look_left_animation_step = 3
                self.look_left_animation_timer.cancel()
                self.look_left_animation_timer = self.create_timer(1.2, self.updateLookLeftAnimation) # 1.2 seconds
            elif self.look_left_animation_step == 3:
                self.updateMatrix("look_left_blink_interim")
                self.look_left_animation_step = 0
                self.look_left_animation_timer.cancel() 
                self.look_left_animation_timer = self.create_timer(0.03, self.updateLookLeftAnimation) # 0.03 seconds
        else:
            self.look_left_animation_step = 0
    
    # LOOK RIGHT ANIMATION
    def updateLookRightAnimation(self):
        if self.allow_look_right_animation and self.init_procedure == False:
            if self.look_right_animation_step == 0:
                self.updateMatrix("look_right")
                self.look_right_animation_step = 1
                self.look_right_animation_timer.cancel() 
                self.look_right_animation_timer = self.create_timer(4.0, self.updateLookRightAnimation) # 4 seconds
            elif self.look_right_animation_step == 1:
                self.updateMatrix("look_right_blink_interim")
                self.look_right_animation_step = 2
                self.look_right_animation_timer.cancel()  
                self.look_right_animation_timer = self.create_timer(0.02, self.updateLookRightAnimation) # 0.02 seconds
            elif self.look_right_animation_step == 2:
                self.updateMatrix("look_right_blink")
                self.look_right_animation_step = 3
                self.look_right_animation_timer.cancel()
                self.look_right_animation_timer = self.create_timer(1.2, self.updateLookRightAnimation) # 1.2 seconds
            elif self.look_right_animation_step == 3:
                self.updateMatrix("look_right_blink_interim")
                self.look_right_animation_step = 0
                self.look_right_animation_timer.cancel() 
                self.look_right_animation_timer = self.create_timer(0.03, self.updateLookRightAnimation) # 0.03 seconds
        else:
            self.look_right_animation_step = 0
        

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