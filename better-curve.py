import sys

import plotter


p = plotter.Plotter(
        # hard to measure solo
        160.97
        # height doesn't really matter
        #, 3*12*2.54
        , 160.97
        # caliper-measured
        , 1.375
        , '/dev/serial/by-id/usb-SchmalzHaus_EiBotBoard-if00')

units = sys.argv[1]
p.move_to_relative([0, units])
p.move_to_relative([units, 0])

counter = 0
while(1):
    p.move_to_relative([-1, 0])
    p.move_to_relative([-units+counter+1, -counter-1])
    counter += 1

    p.move_to_relative([0, -1])
    p.move_to_relative([units-counter-1, counter+1])
    counter += 1


'''
p.move_to_relative([0, units])
p.move_to_relative([units, 0])

counter = 0
while(1):
    # second pass, this doesn't subtract enough to get back to the y axis..
    p.move_to_relative([-units+counter, -1])
    counter += 1

    p.move_to_relative([0, -1])
    p.move_to_relative([units-counter, counter+1])
    counter += 1

    if counter == units:
        break
'''
