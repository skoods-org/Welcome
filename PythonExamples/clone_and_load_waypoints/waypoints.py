import airsim
import numpy as np
import time
import pickle


class Waypoints:
    def __init__(self, client, file_path="test.pickle", frequency=10.0):
        self.client = client
        self.waypoints_array = []
        self.waypoints_file_path = file_path
        self.frequency = frequency

    def save_waypoints_array(self):
        # pip save waypoints
        print ('\tSaving waypoints to pickle file.')
        with open(self.waypoints_file_path,"wb") as f:
            pickle.dump(self.waypoints_array, f)
        print("\tSuccess! %d waypoints saved." % (len(self.waypoints_array)))

    def load_waypoints_array(self):
        # pip load waypoints back as a test
        with open(self.waypoints_file_path, "rb") as f:
            self.waypoints_array = pickle.load(f)
        print("\tSuccess! %d waypoints loaded." % (len(self.waypoints_array)))

    def clone_waypoint(self):

        # Get simulation ground truth + lidar
        ground_truth_kinematics = self.client.simGetGroundTruthKinematics()
        ground_truth_environment = self.client.simGetGroundTruthEnvironment()
        car_state = self.client.getCarState()
        # lidar_data = self.client.getLidarData()
        
        # Create dictionary with waypoint data
        waypoint_dic = {
            "ground_truth_kinematics" : ground_truth_kinematics,
            "ground_truth_environment" : ground_truth_environment,
            "car_state" : car_state
            # "lidar_data" : lidar_data
            }
        # append waypoint dictionary to array
        self.waypoints_array.append(waypoint_dic)
        print("\t%d waypoints cloned." % (len(self.waypoints_array)))

        # wait a little bit
        time.sleep(1./self.frequency)



    def return_waypoints_array(self):
        return self.waypoints_array
    



'''
print(self.waypoints_array[2]) # Check if it's loading

{'ground_truth_kinematics': <KinematicsState> {   'angular_acceleration': <Vector3r> {   'x_val': 0.0,
    'y_val': 0.0,
    'z_val': 0.0},
    'angular_velocity': <Vector3r> {   'x_val': 0.0,
    'y_val': 0.0,
    'z_val': 0.0},
    'linear_acceleration': <Vector3r> {   'x_val': 0.0,
    'y_val': 0.0,
    'z_val': 0.0},
    'linear_velocity': <Vector3r> {   'x_val': 39.70000076293945,
    'y_val': -77.4000015258789,
    'z_val': 1.3134411573410034},
    'orientation': <Quaternionr> {   'w_val': 0.7071062326431274,
    'x_val': 2.188803773606196e-05,
    'y_val': -2.1888072296860628e-05,
    'z_val': -0.7071073651313782},
    'position': <Vector3r> {   'x_val': -2.441406195430318e-06,
    'y_val': 0.0,
    'z_val': 0.13665451109409332}},
    
    'ground_truth_environment': <EnvironmentState> {   'air_density': 1.2104853391647339,
    'air_pressure': 99844.4609375,
    'geo_point': <GeoPoint> {   'altitude': 123.9804916381836,
    'latitude': 47.64111136418785,
    'longitude': -122.13913305496891},
    'gravity': <Vector3r> {   'x_val': 0.0,
    'y_val': 0.0,
    'z_val': 9.806650161743164},
    'position': <Vector3r> {   'x_val': -2.441406195430318e-06,
    'y_val': 0.0,
    'z_val': 0.13665451109409332},
    'temperature': 287.3441467285156},
    
    'car_state': <CarState> {   'gear': 0,
    'handbrake': False,
    'kinematics_estimated': <KinematicsState> {   'angular_acceleration': <Vector3r> {   'x_val': 0.0,
    'y_val': 0.0,
    'z_val': 0.0},
    'angular_velocity': <Vector3r> {   'x_val': 0.0,
    'y_val': 0.0,
    'z_val': 0.0},
    'linear_acceleration': <Vector3r> {   'x_val': 0.0,
    'y_val': 0.0,
    'z_val': 0.0},
    'linear_velocity': <Vector3r> {   'x_val': 39.70000076293945,
    'y_val': -77.4000015258789,
    'z_val': 1.3134411573410034},
    'orientation': <Quaternionr> {   'w_val': 0.7071062326431274,
    'x_val': 2.188803773606196e-05,
    'y_val': -2.1888072296860628e-05,
    'z_val': -0.7071073651313782},
    'position': <Vector3r> {   'x_val': -2.441406195430318e-06,
    'y_val': 0.0,
    'z_val': 0.13665451109409332}},
    'maxrpm': 12000.0,
    'rpm': 0.0,
    'speed': -0.0,
    'timestamp': 1540966787685018700}}
'''