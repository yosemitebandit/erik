'''
emergent-curve.py
draws straight lines between points on the x and y axes to form curves
usage, 10cm axes with a step of 1/5cm:
    $ python emergent-curve.py 10 5 1 1
'''
import sys

import plotter

if '--simulate' in sys.argv:
    simulate_plot = True
else:
    simulate_plot = False

p = plotter.Plotter(
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
# x and y directions
direction = [int(sys.argv[3]), int(sys.argv[4])]

p.move_to_relative([0, direction[1]*units])
p.move_to_relative([direction[0]*units, 0])

counter = 0
while(1):
    p.move_to_relative([-direction[0]/scaling, 0])

    p.move_to_relative([direction[0]*(-units+(counter+1)/scaling)
        , -direction[1]*(counter+1)/scaling])
    counter += 1


    p.move_to_relative([0, -direction[1]/scaling])

    p.move_to_relative([direction[0]*(units-(counter+1)/scaling)
        , direction[1]*(counter+1)/scaling])
    counter += 1

    if counter >= units*scaling:
        break

# wraps things up
p.finish()
