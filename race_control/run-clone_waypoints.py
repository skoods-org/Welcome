import pickle, airsim, waypoints
from pynput import keyboard # Run $pip install pynput in the Anaconda prompt

# Initialize
airsim.wait_key('Press any key to start.')
client = airsim.CarClient()
client.confirmConnection()
waypoints = waypoints.Waypoints()

# Create interruption with END key
break_program = False # helper var
def on_press(key):
    global break_program
    print (key)
    if key == keyboard.Key.end:
        break_program = True
        #### AFTER PRESSING END ####
        waypoints.save_waypoints_list(file_name="waypoints.pickle")
        #### END ####
        return False

with keyboard.Listener(on_press=on_press) as listener:
    while break_program == False:
        #### MAIN CODE ####
        waypoints.clone_waypoint(client, sample_time = 0.01)
        #### END ####

    listener.join()
