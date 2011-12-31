'''
iris.py
draws two emergent curves opposite one another, forming an 'iris'
usage, 10cm axes with a step of 1/5cm
    $ python iris.py 10 5
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

def draw_curve():
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

direction = [1, 1]
# pen starts at the corner; draws the bounds first
p.move_to_relative([0, -direction[1]*units])
p.move_to_relative([0, direction[1]*units])
p.move_to_relative([direction[0]*units, 0])
draw_curve()

# pen starts at the corner; move to the opposite spot
p.move_to_relative([0, -direction[1]*units])
# no idea why the next line is not needed
#p.move_to_relative([-direction[0]*units, 0])

# flip the direction
direction = [-1 for m in direction]
draw_curve()

# wraps things up
p.finish()
