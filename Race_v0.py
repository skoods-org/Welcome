import airsim
import time

import os
import numpy as np

# connect to the AirSim simulator 
client = airsim.CarClient()
client.confirmConnection()

# enable API contro (control from the code)
# client.enableApiControl(True)
# car_controls = airsim.CarControls()

time.sleep(10)   # let car drive a bit