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

#### MAIN CODE ####
waypoints.load_waypoints_array() # load values from picle file
waypoints_returned = waypoints.return_waypoints_array()
# print(waypoints_returned[2])
# do something with waypoints
#### END ####


# get position
# ground_truth_position = ground_truth_kinematics.position
# print(ground_truth_position)
# get orientation X, Y, Z
# pitch, roll, yaw = airsim.utils.to_eularian_angles(ground_truth.orientation)
# print(pitch, roll, yaw)
