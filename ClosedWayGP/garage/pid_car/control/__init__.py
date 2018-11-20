##########################################
### Skoods.org -> Self-Racing Car Team ###
##########################################

import math
from garage.pid_car.control import pid
from skoods import utils


# Create PIDControl generic class
class PIDControl:
    def __init__(self, car, pid_params, sample_time, limits):
        self.car = car
        self.pid_params = pid_params
        self.sample_time = sample_time
        self.limits = limits
        self.pid_controller = pid.PID(self.pid_params[0], self.pid_params[1], self.pid_params[2])
        self.pid_controller.setSampleTime(self.sample_time)
        self.initial_search_index = 0
        self.DELTA_INITIAL_SEARCH_INDEX = 300 # Avoid searching all waypoints. We can make it dinamic by getting time stamps.

    def updateNearestIndex(self, car, waypoints_x, waypoints_y):
        # Funtion to return nearest point from waypoints to car position
        length = len(waypoints_x)
        final_search_index = self.initial_search_index + self.DELTA_INITIAL_SEARCH_INDEX
        if final_search_index > length-1:
            final_search_index = -1 # define as last element

        dx = [car.state.kinematics_estimated.position.x_val - iwpx for iwpx in waypoints_x[self.initial_search_index:final_search_index]]  
        dy = [car.state.kinematics_estimated.position.y_val - iwpy for iwpy in waypoints_y[self.initial_search_index:final_search_index]]
        d = [ix ** 2 + iy ** 2 for (ix, iy) in zip(dx, dy)]
        nearest_waypoint_distance = min(d)
        nearest_waypoint_index = d.index(nearest_waypoint_distance)
        nearest_waypoint_index += self.initial_search_index

        # Check end of waypoints index
        if nearest_waypoint_index >= length-2:
            self.initial_search_index = 0
            keep_racing = False
        else:
            keep_racing = True
            self.initial_search_index = nearest_waypoint_index
        
        keep_racing = True # Force

        return nearest_waypoint_index, keep_racing


    def limitOutput(self, output):
        # Limit the output of the controller based on limitations of the car
        if output < self.limits[0]:
            output = self.limits[0]
            self.pid_controller.output = output
        elif output > self.limits[1]:
            output = self.limits[1]
            self.pid_controller.output = output
        return output


class PIDThrottleControl(PIDControl):
    def __init__(self, car_state, pid_params, sample_time, limits):
        PIDControl.__init__(self, car_state, pid_params, sample_time, limits)

    def setTargetValue(self, car_state, waypoints_x, waypoints_y, waypoints_v):
        # Set the value of the target by returning the speed of the nearest waypoint
        nearest_waypoint_index, keep_racing = self.updateNearestIndex(car_state, waypoints_x, waypoints_y)
        if keep_racing:
            # Avoid low speed set points, specialy during the start
            if waypoints_v[nearest_waypoint_index] > 2.0:
                self.pid_controller.SetPoint = waypoints_v[nearest_waypoint_index]
            else:
                self.pid_controller.SetPoint = 2.0
        return keep_racing

    def getControlsFromPID(self, car):
        # Return the value of the controls after updating the PID
        self.pid_controller.update(car.state.speed)
        output = self.pid_controller.output
        output = self.limitOutput(output)
        # Define throttle and brake
        if output < 0.0:
            car.controls.throttle = 0.0
            car.controls.brake = output
        if output >= 0.0:
            car.controls.brake = 0.0
            car.controls.throttle = output
        return car


class PIDSteeringControl(PIDControl):
    def __init__(self, car, pid_params, sample_time, limits):
        PIDControl.__init__(self, car, pid_params, sample_time, limits)

    def setTargetValue(self):
        # The target of steering is always 0, and the error is the distance from the car to the nearest point
        self.pid_controller.SetPoint = 0.0


    def getControlsFromPID(self, car, waypoints_x, waypoints_y):
        # Return the value of the controls after updating the PID
        nearest_waypoint_index, keep_racing = self.updateNearestIndex(car, waypoints_x, waypoints_y)
        if keep_racing:
            delta_error = utils.get_distance_of_point_to_line([car.state.kinematics_estimated.position.x_val, car.state.kinematics_estimated.position.y_val],
                                                        [waypoints_x[nearest_waypoint_index], waypoints_y[nearest_waypoint_index]],
                                                        [waypoints_x[nearest_waypoint_index+1], waypoints_y[nearest_waypoint_index+1]])
            # Get direction of steering (+ or -?)
            # Change coordinate system
            point_A = [waypoints_x[nearest_waypoint_index], waypoints_y[nearest_waypoint_index]]
            point_B = [waypoints_x[nearest_waypoint_index+1], waypoints_y[nearest_waypoint_index+1]]  # define the increment of the index depending on the sampling time.
            point_P = [car.state.kinematics_estimated.position.x_val, car.state.kinematics_estimated.position.y_val]
            # point_A_line = [point_A[0]-point_A[0], point_A[1]-point_A[1]] # This will be the origin (0.0, 0.0)
            point_B_line = [point_B[0]-point_A[0], point_B[1]-point_A[1]]
            point_P_line = [point_P[0]-point_A[0], point_P[1]-point_A[1]]
            # BP cross product
            cross_product_BP = point_B_line[0]*point_P_line[1]-point_P_line[0]*point_B_line[1]
            # Check direction
            if cross_product_BP < 0:
                delta_error *= -1

            # Update PID and set controls
            self.pid_controller.update(delta_error)
            output = self.pid_controller.output
            output = self.limitOutput(output)
            car.controls.steering = output

        return car, keep_racing

