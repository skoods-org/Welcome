import airsim, car, waypoints, control

# SIMULATION
# Connect to the AirSim simulator
airsim.wait_key('Press any key to start.')
client = airsim.CarClient()
client.confirmConnection()
client.enableApiControl(True)

# INITIALIZE CAR
car = car.CarState()

# PLANNING: Load waypoints lists of: x, y, yaw and v (we are not using yaw)
waypoints = waypoints.Waypoints()
waypoints_x, waypoints_y, waypoints_yaw, waypoints_v = waypoints.load_waypoints_lists(file_name="waypoints.pickle")

# CONTROL
# Initialize Throttle PID
throttle_pid_params = [0.7, 0.0, 0.1] # PID params
throttle_sample_time = 0.05 # seconds
throttle_limits = [-1.0, 1.0] # Lower and Upper limits
throttle_controller = control.PIDThrottleControl(throttle_pid_params, throttle_sample_time, throttle_limits)
# Initialize Steering PID
steering_pid_params = [0.07, 0.01, 0.2] # PID params
steering_sample_time = 0.05 # seconds
steering_limits = [-0.5, 0.5] # Lower and Upper limits
steering_controller = control.PIDSteeringControl(steering_pid_params, steering_sample_time, steering_limits)
steering_controller.setTargetValue() # It's always zero (different from Throttle PID)

# RACE
while(True):
    # Run Throttle PID
    car.updateSimGT(client) # Update car state: x, y, yaw, v (we are not using yaw)
    throttle_controller.setTargetValue(car, waypoints_x, waypoints_y, waypoints_v) # Set goal each interaction, as speed target will change
    car = throttle_controller.getControls(car) # Return controls after running PID (this method is different for each PID type)
    car.setCarControls(client) # Send controls to simulation
    # Run Steering PID
    car.updateSimGT(client) # Update car state: x, y, yaw, v (we are not using yaw)
    car = steering_controller.getControls(car, waypoints_x, waypoints_y) # Return controls after running PID (this method is different for each PID type)
    car.setCarControls(client) # Send controls to simulation


