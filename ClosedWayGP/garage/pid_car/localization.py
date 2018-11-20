##########################################
### Skoods.org -> Self-Racing Car Team ###
##########################################

import airsim


def updateState(car):
    '''
    Here we are returning data from the simulation.
    In the future, we will have to update the state
    using data from sensors. That's why we have this
    simple funtion here.
    '''
    return car.client.getCarState(car.name)


'''
CARSTATE STRUCTURE
<CarState> {   'gear': 1,
    'handbrake': False,
    'kinematics_estimated': <KinematicsState> {   'angular_acceleration': <Vector3r> {   'x_val': 0.00029464520048350096,
    'y_val': -0.06526550650596619,
    'z_val': 0.0022375881671905518},
    'angular_velocity': <Vector3r> {   'x_val': 2.47272018896183e-05,
    'y_val': -0.0028818382415920496,
    'z_val': 0.0002823330869432539},
    'linear_acceleration': <Vector3r> {   'x_val': -0.20411361753940582,
    'y_val': 5.819011688232422,
    'z_val': -6.0460195527412e-05},
    'linear_velocity': <Vector3r> {   'x_val': 39.90984344482422,
    'y_val': -83.43799591064453,
    'z_val': 1.313422679901123},
    'orientation': <Quaternionr> {   'w_val': 0.7192735075950623,
    'x_val': -0.0029264732729643583,
    'y_val': -0.0030786246061325073,
    'z_val': -0.6947140693664551},
    'position': <Vector3r> {   'x_val': -0.6134936213493347,
    'y_val': -64.33607482910156,
    'z_val': 0.13678878545761108}},
    'maxrpm': 12000.0,
    'rpm': 1045.26123046875,
    'speed': 5.9793381690979,
    'timestamp': 1541474232806460800}
'''