import airsim
import numpy as np
# import time
# import cv2
import pickle
from pynput import keyboard # Run $pip install pynput in the Anaconda prompt
from waypoints import Waypoints

# Connect to the AirSim simulation and create Waypoints object
client = airsim.CarClient()
client.confirmConnection()

#### INITIALIZE OBJECTS AND VARIABLES ####
waypoints = Waypoints(client=client, frequency=10.0)
airsim.wait_key('Press any key to start.') # instructions
#### END ####

# Create interruption with END key
# helper var
break_program = False
def on_press(key):
    global break_program
    print (key)
    if key == keyboard.Key.end:
        break_program = True
        #### AFTER PRESSING END ####
        waypoints.save_waypoints_array()
        #### END ####
        return False

with keyboard.Listener(on_press=on_press) as listener:
    while break_program == False:
        #### MAIN CODE ####
        waypoints.clone_waypoint()
        #### END ####

    listener.join()


# get position
# ground_truth_position = ground_truth_kinematics.position
# print(ground_truth_position)
# get orientation X, Y, Z
# pitch, roll, yaw = airsim.utils.to_eularian_angles(ground_truth.orientation)
# print(pitch, roll, yaw)
