##########################################
### Skoods.org -> Self-Racing Car Team ###
##########################################

import os, time, pickle, airsim, math
from pynput import keyboard # Run $pip install pynput in the Anaconda prompt
from skoods import utils


class Waypoints:
    def __init__(self, car_name):
        self.waypoints_list = []
        self.current_time = time.time()
        self.last_time = self.current_time
        self.past_x_val = 0.0
        self.past_y_val = 0.0
        self.car_name = car_name

    def getCurrentWaypoint(self, car, sample_time):
        # Get and append waypoint after reaching sample time
        self.current_time = time.time()
        delta_time = self.current_time - self.last_time
        car_state = car.client.getCarState(car.name)
        x_val = car_state.kinematics_estimated.position.x_val
        y_val = car_state.kinematics_estimated.position.y_val
        # Record waypoints only 10cm of distance from past waypoint, otherwise can return same waypoint. You can change if you want to.
        if utils.distance_of_two_points(x_val, y_val, self.past_x_val, self.past_y_val) > 0.1:
            distance_bool = True
        else:
            distance_bool = False
        # also take in consideration sample time
        if ((delta_time >= sample_time) and distance_bool == True):
            self.waypoints_list.append(car_state)
            self.last_time = self.current_time
        self.past_x_val = x_val
        self.past_y_val = y_val


    def saveWaypointsToFile(self, filename):
        print (self.car_name + " || WAYPOINTS: Saving waypoints to pickle file.")
        with open(os.path.join(filename),"wb") as f:
            pickle.dump(self.waypoints_list, f)
        print(self.car_name + " || WAYPOINTS: Success! %d waypoints saved to disk." % (len(self.waypoints_list)))
 
    def recordWaypointsToFile(self, car, sample_time, filename):
        # Press END key to complete the recording
        break_program = False
        print(self.car_name + " || PLANNING: Press END to save waypoints to file after driving.")
        def on_press(key):
            global break_program
            # print (key)
            if key == keyboard.Key.end:
                break_program = True
                # After pressing end, run...
                self.saveWaypointsToFile(filename)
                return False
        with keyboard.Listener(on_press=on_press) as listener:
            while break_program == False:
                # Before pressing end, run...
                self.getCurrentWaypoint(car, sample_time)
            listener.join()

    def loadWaypointsFromFile(self, filename):
        with open(os.path.join(filename), "rb") as f:
            self.waypoints_list = pickle.load(f)
        print(self.car_name + " || WAYPOINTS: Success! %d waypoints loaded from disk." % (len(self.waypoints_list)))

    def waypointsToLists(self, waypoints_correction):
        # Waypoints are objects. Here we are transforming them to lists.
        waypoints_x, waypoints_y, waypoints_v = [], [], []
        # FUTURE: waypoints_x, waypoints_y, waypoints_yaw, waypoints_v = [], [], [], []
        for each_waypoint in self.waypoints_list:
            waypoints_x.append(each_waypoint.kinematics_estimated.position.x_val) # Must apply correction when racing with more then one car because of initial position change for the grid.
            waypoints_y.append(each_waypoint.kinematics_estimated.position.y_val)
            # FUTURE: _, _, yaw_val = airsim.utils.to_eularian_angles(each_waypoint.kinematics_estimated.orientation) # NED coord
            # FUTURE: waypoints_yaw.append(yaw_val)
            waypoints_v.append(each_waypoint.speed) # m/s
        return waypoints_x, waypoints_y, waypoints_v
        # FUTURE: return waypoints_x, waypoints_y, waypoints_yaw, waypoints_v


class Behavior:
    def __init__(self, car):
        self.car = car
        self.mode = 'START'
        print(self.car.name + " || BEHAVIOR: Mode = START")

    def setCarBehavior(self):
        # You can create more modes here
        x_val = self.car.state.kinematics_estimated.position.x_val
        y_val = self.car.state.kinematics_estimated.position.y_val
        dist_from_start_point = math.sqrt(x_val**2 + y_val**2)
        if dist_from_start_point > 1.0 and self.mode != 'CRUZE':
            self.mode = 'CRUZE'
            print(self.car.name + " || BEHAVIOR: Mode = CRUZE")

