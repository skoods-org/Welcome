import airsim

import time
import os
import numpy as np

# Connect to the AirSim simulator.
client = airsim.CarClient()
client.confirmConnection()

# Enable API control.
# If you don´t call the client.enableApiControl(True) function,
# you are able to control the car from the simulation using the arrows.
# client.enableApiControl(True)
# car_controls = airsim.CarControls()

while(True):

    # Get state of the car
    car_state = client.getCarState()
    '''
    Example of output after printing out car_state
    <CarState> {
        'gear': 0,
        'handbrake': False,
        'kinematics_estimated': <KinematicsState> {
            'angular_acceleration': <Vector3r> {
                'x_val': 0.0,
                'y_val': 0.0,
                'z_val': 0.0
                },
            'angular_velocity': <Vector3r> {
                'x_val': 0.0,
                'y_val': 0.0,
                'z_val': 0.0
                },
            'linear_acceleration': <Vector3r> {
                'x_val': 0.0,
                'y_val': 0.0,
                'z_val': 0.0
                },
            'linear_velocity': <Vector3r> {
                'x_val': 119.0,
                'y_val': 0.0,
            'z_val': 1.777748942375183
            },
            'orientation': <Quaternionr> {
                'w_val': 0.7071051597595215,
                'x_val': -2.0325323646375182e-07,
                'y_val': -2.1821526274834468e-07,
                'z_val': -0.7071084380149841
                },
            'position': <Vector3r> {
                'x_val': 4.8828122089616954e-05,
                'y_val': -4.4736862037098035e-05,
                'z_val': 0.5828688740730286
                }
            },
        'maxrpm': 5700.0,
        'rpm': 0.0,
        'speed': -0.0,
        'timestamp': 1540404358196773800
        }
    '''
    # Get state of the car and print out the Speed and Gear
    print(car_state)
    time.sleep(1)

#restore to original state
client.reset()

client.enableApiControl(False)


            
