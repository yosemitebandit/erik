'''
flutterby.py
draws two emergent curves touching one another, forming a butterfly of sorts
usage, 10cm axes with a step of 1/5cm
    $ python flutterby.py 10 0.2
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
initial_position = [160.97/2, 160.97/2]

full_path = []
# the first quadrant
curve = Emergent(axis_length, step_size, initial_position, quadrant=1)
path = curve.generate_path()
full_path.extend(path)

# the third quadrant
curve = Emergent(axis_length, step_size, initial_position, quadrant=3)
path = curve.generate_path()
full_path.extend(path)


# plot 'em
for point in full_path:
    plotter.move_to(point)

# wraps things up with the sim
plotter.finish()
