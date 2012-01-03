'''
single-curve.py
draw a single bezier curve, mostly for testing
usage, p0 at start; other points described relatively
    $ python single-curve.py 3,10 34,8 30,1
'''
import math
import sys

import erik 

if '--simulate' in sys.argv:
    simulate_plot = True
else:
    simulate_plot = False

plotter = erik.Plotter(
    # motor separation..still not quite sure this is right
    160.97
    # height is arbitrary but seems to affect the skew of things
    , 160.97
    # caliper-measured motor radius
    , 1.375
    # path to my controller
    , serial_path='/dev/serial/by-id/usb-SchmalzHaus_EiBotBoard-if00'
    # simulating this run?
    , simulate=simulate_plot
)

def _convert_to_point(point):
    return [plotter.initial_position[0] + float(point.split(',')[0])
            , plotter.initial_position[1] + float(point.split(',')[1])]

p1 = _convert_to_point(sys.argv[1])
p2 = _convert_to_point(sys.argv[2])
p3 = _convert_to_point(sys.argv[3])

# first set of control points
control_group = [[plotter.initial_position, p1, p2, p3]]

if '--control' in sys.argv:
    # draw the ctrl points
    plotter.move_to(p1)
    plotter.move_to(p2)
    plotter.move_to(p3)

    # back to start
    plotter.move_to(plotter.initial_position)


# some utilities
def find_distance(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def find_angle(a, b):
    return math.atan((a[1] - b[1]) / (a[0] - b[0]))


# de Casteljau - iteratively find control points
step_fraction = 0.05
distance_limit = 0.1
# calculate control points until we go under some distance limit
k = 0  # kth subsection run
while(1):
    subsected_points = []
    if k == 0:
        # first run, we'll drop one point in the subsection routine
        iterations = len(control_group[0]) - 1
    else:
        # subsequent runs end with one less point than the original ctrl points
        iterations = len(control_group[0]) - 1

    for i in range(iterations):
        # find distance between two control points
        distance = find_distance(control_group[k][i+1], control_group[k][i])

        # find angle between two control points 
        angle = find_angle(control_group[k][i+1], control_group[k][i])
        # above math is busted if control lines forming a V rather than a ^
        # need to do some quadarant fix or somethin..

        # the subsected point is then here:
        subsected_points.append([
            control_group[k][i][0] + step_fraction * distance 
                * math.cos(angle)
            , control_group[k][i][1] + step_fraction * distance 
                * math.sin(angle)
        ])

    # always hold that last control point
    subsected_points.append(control_group[0][-1])

    if find_distance(subsected_points[-2], subsected_points[-1]) < distance_limit:
        break
    
    k += 1
    control_group.append(subsected_points)


# plot curve points
for g in control_group:
    plotter.move_to(g[0])


# wraps things up with the sim
plotter.finish()
