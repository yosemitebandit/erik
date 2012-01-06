'''
flutterby.py
draws two emergent curves touching one another, forming a butterfly of sorts
usage, 10cm axes with a step of 1/5cm and pull the 'wings' 30deg 
    $ python flutterby.py 10 0.2 30
'''
import math
import sys

from emergent_curve import Emergent
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

axis_length = float(sys.argv[1])
step_size = float(sys.argv[2])
angle = -1*math.pi/180*float(sys.argv[3])

initial_position = [160.97/2, 160.97/2]

# the first quadrant
curve = Emergent(axis_length, step_size, initial_position, quadrant=1)
path = curve.generate_path()

# rotate the 'wings' a bit
path_rotated = []
for point in path:
    if point[0] == initial_position[0]:
        # on the y-axis
        angle_adjusted = angle + math.pi/2
    else:
        angle_adjusted = angle

    d = math.sqrt((initial_position[0] - point[0])**2
        + (initial_position[1] - point[1])**2)

    path_rotated.append([
        initial_position[0] + d*math.cos(angle_adjusted)
        , initial_position[1] + d*math.sin(angle_adjusted)
    ])

# reflect
path_reflected = []
for point in path_rotated:
    delta_x = point[0] - initial_position[0]
    path_reflected.append([
        initial_position[0] - delta_x
        , point[1]
    ])


full_path = []
full_path.extend(path_rotated)
full_path.extend(path_reflected)


# plot 'em
for point in full_path:
    plotter.move_to(point)

# wraps things up with the sim
plotter.finish()
