import os, time, pickle, airsim

# We can save, clone and load waypoints.
class Waypoints:
    def __init__(self, file_path="waypoints.pickle"):
        # Initialize variables
        self.waypoints_list = []
        self.waypoints_file_path = file_path
        self.current_time = time.time()
        self.last_time = self.current_time
        self.dir_path = os.path.dirname(__file__)

    # Clone the current state of the car in the simulation using Ground Truth data
    def clone_waypoint(self, client, sample_time = 0.1):

        # Handle sample time
        self.current_time = time.time()
        delta_time = self.current_time - self.last_time

        # Get waypoint after reaching sample time
        if (delta_time >= sample_time):
            # Get simulation ground truth
            # Create dictionary with waypoint data
            waypoint_dict = {
                "ground_truth_kinematics"   : client.simGetGroundTruthKinematics(),
                "ground_truth_environment"  : client.simGetGroundTruthEnvironment(),
                "car_state"                 : client.getCarState()
                }
            # Append to list
            self.waypoints_list.append(waypoint_dict)
            
            print("\tX: %.2f, Y: %.2f, Delta time: %.3f, Number of waypoints: %d." % (
                waypoint_dict['ground_truth_kinematics'].position.x_val,
                waypoint_dict['ground_truth_kinematics'].position.y_val,
                delta_time,
                len(self.waypoints_list)))
            
            self.last_time = self.current_time


    # Save all the waypoints inside waypoints_list to disk as a pickle file
    def save_waypoints_list(self, file_name="waypoints.pickle"):
        print ('\tSaving waypoints to pickle file.')
        with open(os.path.join(self.dir_path, file_name),"wb") as f:
            pickle.dump(self.waypoints_list, f)
        print("\tSuccess! %d waypoints saved." % (len(self.waypoints_list)))

    # Load waypoint from pickle file on disk
    def load_waypoints(self, file_name="waypoints.pickle"):
        with open(os.path.join(self.dir_path, file_name), "rb") as f:
            self.waypoints_list = pickle.load(f)
        print("\tSuccess! %d waypoints loaded." % (len(self.waypoints_list)))

    # Load waypoints but not as a list of objects, but as individual lists
    def load_waypoints_lists(self, file_name="waypoints.pickle"): # Return lists of x, y, yaw, v (not the list of waypoint objects)
        self.load_waypoints(file_name=file_name)
        # Initialize waypoint lists
        waypoints_x, waypoints_y, waypoints_yaw, waypoints_v = [], [], [], []
        # Append values
        for each_waypoint in self.waypoints_list:
            waypoints_x.append(each_waypoint['ground_truth_kinematics'].position.x_val)
            waypoints_y.append(each_waypoint['ground_truth_kinematics'].position.y_val)
            _, _, yaw_val = airsim.utils.to_eularian_angles(each_waypoint['ground_truth_kinematics'].orientation) # NED coord
            waypoints_yaw.append(yaw_val)
            waypoints_v.append(each_waypoint['car_state'].speed) # m/s
        return waypoints_x, waypoints_y, waypoints_yaw, waypoints_v

