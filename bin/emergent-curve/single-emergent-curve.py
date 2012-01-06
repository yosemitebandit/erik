'''
single-emergent-curve.py
draws straight lines between points on the x and y axes to form curves
usage, 10cm axes with a step of 0.2cm in the second quadrant:
    $ python emergent-curve.py 10 0.2 2
'''
import sys

from emergent_curve import Emergent
import erik

if '--simulate' in sys.argv:
    simulate_plot = True
else:
    simulate_plot = False

p = erik.Plotter(
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
quadrant = sys.argv[3]

initial_position = [160.97/2, 160.97/2]


curve = Emergent(axis_length, step_size, initial_position, quadrant=quadrant)
path = curve.generate_path()

for point in path:
    p.move_to(point)

# wraps things up with the sim
p.finish()
