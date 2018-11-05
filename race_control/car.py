import airsim

class CarState:
    # Initialize car controls variable to hold the values
    def __init__(self):
        self.car_controls = airsim.CarControls() 

    # Load Simulation Ground Truth values (kind of cheating), as we don't have LOCALIZATION yet.
    def updateSimGT(self, client):
        ground_truth_kinematics = client.simGetGroundTruthKinematics()
        ground_truth_environment = client.simGetGroundTruthEnvironment() # We don't use this var, but it's here :)
        car_state = client.getCarState()

        # Update state: x, y, yaw, v
        self.x = ground_truth_kinematics.position.x_val
        self.y = ground_truth_kinematics.position.y_val
        _, _, self.yaw = airsim.utils.to_eularian_angles(ground_truth_kinematics.orientation) # NED coord
        self.v = car_state.speed # m/s

    # Send controls to simulation    
    def setCarControls(self, client):
        client.setCarControls(self.car_controls)
