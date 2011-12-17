'''
emergent-curve.py
draws straight lines between points on the x and y axes to form curves
usage, 10cm axes with a step of 1/5cm:
    $ python emergent-curve.py 10 5
'''
import sys

import plotter

p = plotter.Plotter(
        # motor separation..still not quite sure this is right
        160.97
        # height is arbitrary but seems to affect the skew of things
        , 160.97
        # caliper-measured motor radius
        , 1.375
        # path to my controller
        , '/dev/serial/by-id/usb-SchmalzHaus_EiBotBoard-if00')

units = int(sys.argv[1])
scaling = float(sys.argv[2])

p.move_to_relative([0, units])
p.move_to_relative([units, 0])

counter = 0
while(1):
    p.move_to_relative([-1/scaling, 0])
    p.move_to_relative([-units+(counter+1)/scaling, -(counter+1)/scaling])
    counter += 1

    p.move_to_relative([0, -1/scaling])
    p.move_to_relative([units-(counter+1)/scaling, (counter+1)/scaling])
    counter += 1

    if counter >= units*scaling:
        break
