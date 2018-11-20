##########################################
### Skoods.org -> Self-Racing Car Team ###
##########################################

import math

def distance_of_two_points(x0, y0, x1, y1):
    return math.sqrt((x0-x1)**2 + (y0-y1)**2)

def get_distance_of_point_to_line(point, line_point_0, line_point_1):
    # Get the distânce of the car position to the trajectory, calculating steering error
    distance = 0.0
    # Point
    x0 = point[0]
    y0 = point[1]
    # Line Segment
    x1 = line_point_0[0]
    y1 = line_point_0[1]
    x2 = line_point_1[0]
    y2 = line_point_1[1]
    # equations and checks
    denominator = math.sqrt((y2-y1)**2 + (x2-x1)**2)
    if denominator<0.0000001: # Avoid equal waypoints
        denominator = 0.001
        distance = abs( ((y2-y1)*x0 - (x2-x1)*y0 + x2*y1 - y2*x1) / denominator )
    else:
        distance = abs( ((y2-y1)*x0 - (x2-x1)*y0 + x2*y1 - y2*x1) / denominator )
    return distance