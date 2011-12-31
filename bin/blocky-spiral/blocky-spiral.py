'''
blocky-spiral.py
nested squares, spiraling outward
usage, 10cm final square with a step of 1/2cm:
    $ python emergent-curve.py 10 0.5
'''
import sys

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
        , '/dev/serial/by-id/usb-SchmalzHaus_EiBotBoard-if00'
        # simulating this run?
        , simulate=simulate_plot
    )

units = float(sys.argv[1])
scaling = float(sys.argv[2])

# initialize the side length
side_length = scaling

while(1):
    # clockwise square circle
    p.move_to_relative([side_length, 0])
    p.move_to_relative([0, side_length])
    side_length += scaling

    p.move_to_relative([-side_length, 0])
    p.move_to_relative([0, -side_length])
    side_length += scaling

    if side_length >= units:
        break

# wraps things up with the sim
p.finish()
