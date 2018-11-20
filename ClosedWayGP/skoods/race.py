##########################################
### Skoods.org -> Self-Racing Car Team ###
##########################################

import airsim, math, time


class Race:
    def __init__(self, sample_time):

        self.sample_time = sample_time
        self.cars_race_states = []
        self.laps_completed = []
        self.lap_times = []
        self.past_accum_time = []
        self.client = airsim.CarClient()
        self.client.confirmConnection()

        # Set Mode and Simulation Abstraction
        self.mode_input = input("Type **1** to drive the car by your own and RECORD data (will load the first car), "+ \
                                     "**2** to QUALIFY (will load the first car) or "+ \
                                     "**3** to RACE (accepts multiple cars): ")
        if self.mode_input == '1':
            print("Race || MODE: WAYPONTS RECORDING")
        elif self.mode_input == '2':
            print("Race || MODE: QUALIFY")
        elif self.mode_input == '3':
            print("Race || MODE: RACE")
        else:
            print("Race || Warning - MODE: Not defined")

        if self.mode_input == '2' or self.mode_input == '3':
            pause_simulation_input = input("Type **1** to PAUSE SIMULATION to process data during racing (better performance but takes longer) or "+ \
                                                "**2** to run the racing in REAL-TIME (worse performance but faster): ")
            if  pause_simulation_input == '1': # Pause
                print("Race || SIMULATION: Pause")
                self.pause_simulation = True
                self.accum_time = 0.0
                self.client.simPause(True)
            elif pause_simulation_input == '2': # Real-time
                print("Race || SIMULATION: Real-Time")
                self.pause_simulation = False
                self.client.simPause(False)
            else:
                 print("RACE || Warning - SIMULATION: Not defined")


    def setInitialTime(self):
        self.initial_time = time.time()

    def setCars(self, cars):
        self.cars = cars
        for each_car in self.cars:
            self.cars_race_states.append(-1)
            self.laps_completed.append(0)
            car_dict = {'car_name' : each_car.name}
            self.lap_times.append(car_dict)
            self.past_accum_time.append(0.0)

    def setNumberOfLaps(self, number_of_laps):
        self.number_of_laps = number_of_laps

    def playSimulation(self):
        if self.pause_simulation:
            self.client.simPause(False)
            time.sleep(self.sample_time)
            self.client.simPause(True)
            self.accum_time += self.sample_time
        else:
            self.accum_time = time.time() - self.initial_time

    def updateRaceParameters(self):
        keep_racing = True
        distances_from_start_point = []
        for i, each_car in enumerate(self.cars):
            x_val = each_car.state.kinematics_estimated.position.x_val
            y_val = each_car.state.kinematics_estimated.position.y_val
            distances_from_start_point.append(math.sqrt(x_val**2 + y_val**2))

            if distances_from_start_point[i] > 50.0 and self.cars_race_states[i] == -1:
                self.cars_race_states[i] = 0

            if distances_from_start_point[i] < 2.0 and self.cars_race_states[i] == 0:
                self.cars_race_states[i] = -1
                self.laps_completed[i] += 1
                self.lap_times[i][str(self.laps_completed[i])] = self.accum_time - self.past_accum_time[i]
                self.past_accum_time[i] = self.accum_time
                print(self.lap_times[i])
                if self.laps_completed[i] >= self.number_of_laps:
                    self.cars_race_states[i] = 1
                    if sum(self.cars_race_states) == len(self.cars_race_states):
                        keep_racing = False
                        self.endRace()
        return keep_racing


    def endRace(self):
        print("RACE completed!")
        for each_lap_time in self.lap_times:
            print(each_lap_time)
        print("Upload your code: www.skoods.org")
        self.client.simPause(False)





