import math, pid

# Create PIDControl generic class
class PIDControl:
    def __init__(self, pid_params, sample_time, limits):
        # Initialize variables
        self.pid_params = pid_params
        self.sample_time = sample_time
        self.limits = limits
        # Initialize PID
        self.pid_controller = pid.PID(self.pid_params[0], self.pid_params[1], self.pid_params[2])
        self.pid_controller.clear()
        self.pid_controller.setSampleTime(self.sample_time)

    # Funtion to return nearest point from waypoints to car position
    # We also use the nearest waypoint distance to feed the steering PID controller.
    def updateNearestIndex(self, car, waypoints_x, waypoints_y):
        dx = [car.x - iwpx for iwpx in waypoints_x]  
        dy = [car.y - iwpy for iwpy in waypoints_y]
        d = [ix ** 2 + iy ** 2 for (ix, iy) in zip(dx, dy)]
        nearest_waypoint_distance = min(d)
        nearest_waypoint_index = d.index(nearest_waypoint_distance)
        nearest_waypoint_distance = math.sqrt(nearest_waypoint_distance)
        # Improvement: get the distance not to the nearest point, but to the trajectory.
        return nearest_waypoint_index, nearest_waypoint_distance

    # Limit the output of the controller based on limitations of the car
    def limitOutput(self, output):
        if output < self.limits[0]:
            output = self.limits[0]
            self.pid_controller.output = output
        elif output > self.limits[1]:
            output = self.limits[1]
            self.pid_controller.output = output
        return output


class PIDThrottleControl(PIDControl):
    def __init__(self, pid_params, sample_time, limits):
        PIDControl.__init__(self, pid_params, sample_time, limits)

    # Set the value of the goal by returning the speed of the nearest waypoint
    def setTargetValue(self, car, waypoints_x, waypoints_y, waypoints_v):
        nearest_waypoint_index, _ = self.updateNearestIndex(car, waypoints_x, waypoints_y)
        self.pid_controller.SetPoint = waypoints_v[nearest_waypoint_index]

    # Return the value of the controls after updating the PID
    def getControls(self, car):
        self.pid_controller.update(car.v) # Run the PID
        output = self.pid_controller.output
        output = self.limitOutput(output)
        # Define throttle and brake
        if output < 0.0:
            car.car_controls.throttle = 0.0
            car.car_controls.brake = output
        if output >= 0.0:
            car.car_controls.brake = 0.0
            car.car_controls.throttle = output
        return car


class PIDSteeringControl(PIDControl):
    def __init__(self, pid_params, sample_time, limits):
        PIDControl.__init__(self, pid_params, sample_time, limits)

    # The target of steering is always 0, and the error is the distance from the car to the nearest point
    def setTargetValue(self):
        self.pid_controller.SetPoint = 0.0

    # Return the value of the controls after updating the PID
    def getControls(self, car, waypoints_x, waypoints_y):
        nearest_waypoint_index, nearest_waypoint_distance = self.updateNearestIndex(car, waypoints_x, waypoints_y)

        # GET DIRECTION OF STEERING
        # Change coordinate system
        point_A = [waypoints_x[nearest_waypoint_index], waypoints_y[nearest_waypoint_index]]
        point_B = [waypoints_x[nearest_waypoint_index+1], waypoints_y[nearest_waypoint_index+1]]
        point_P = [car.x, car.y]
        # point_A_line = [point_A[0]-point_A[0], point_A[1]-point_A[1]] # This will be the origin (0.0, 0.0)
        point_B_line = [point_B[0]-point_A[0], point_B[1]-point_A[1]]
        point_P_line = [point_P[0]-point_A[0], point_P[1]-point_A[1]]
        # BP cross product
        cross_product_BP = point_B_line[0]*point_P_line[1]-point_P_line[0]*point_B_line[1]
        # Check direction
        if cross_product_BP < 0:
            nearest_waypoint_distance *= -1

        # Update PID and set controls
        self.pid_controller.update(nearest_waypoint_distance)
        output = self.pid_controller.output
        output = self.limitOutput(output)
        car.car_controls.steering = output

        return car