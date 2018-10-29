import airsim
import numpy as np
import time

# Connect to the AirSim simulator
client = airsim.CarClient()
client.confirmConnection()

airsim.wait_key('Press any key.')

i = 0
current_time_stamp = 0

while(i<2000):
    lidarData = client.getLidarData()
    new_time_stamp = lidarData.time_stamp
    # Check time_stamp to compar with past time_stamp. Avoid processing the same info 2x
    if current_time_stamp != new_time_stamp:

        current_time_stamp = new_time_stamp

        # Check if points exist
        if (len(lidarData.point_cloud) < 3):
            print("\tReading %d: time_stamp: %d No points received from Lidar data" % (i, time_stamp))

        # Transform to np.array of 3D ponits
        else:
            new_points = np.array(lidarData.point_cloud, copy=True, dtype=np.dtype('f4'))
            new_points = np.reshape(new_points, (int(new_points.shape[0]/3), 3))
            if i==0:
                points = new_points
            else:
                points = np.append(points, new_points, axis=0)

        print("\tReading %d: time_stamp: %d number_of_points: %d" % (i, current_time_stamp, points.shape[0]))
        i+=1

    time.sleep(0.0333)

np.savetxt("hd_map_example.xyz", points, fmt='%s')


