'''
curve.py
drawing those 'emergent' curves
..traces every line twice, hm
'''
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

units = 30

p.move_to_relative([0, units])
p.move_to_relative([units, 0])
p.move_to_relative([-units, 0])
p.move_to_relative([0, -units])

for i in range(units):
    # move to lower axis
    p.move_to_relative([i+1, units-i])
    # come back to where it started
    p.move_to_relative([-i-1, -units+i])

    # go to next start point
    p.move_to_relative([0, 1])

