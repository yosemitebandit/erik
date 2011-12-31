'''
move.py
move the pen up, down, left and right
usage, move at 5cm increemnts: 
    $ python move.py 5
'''
import sys

import erik

p = erik.Plotter(
        # hard to measure solo
        #160.97
        159.5
        # height doesn't really matter
        #, 3*12*2.54
        , 160.97
        # caliper-measured
        , 1.375
        , '/dev/serial/by-id/usb-SchmalzHaus_EiBotBoard-if00')

move_distance = float(sys.argv[1])
position = p.position

while(1):
    direction = raw_input('specify a direction (udrl): ')                  

    # adjust the desired x,y coordinates of the pen head                   
    if direction == 'u':                                                   
        p.move_to_relative([0, -move_distance])
    elif direction == 'd':                                                 
        p.move_to_relative([0, move_distance])
    elif direction == 'r':                                                 
        p.move_to_relative([move_distance, 0])
    elif direction == 'l':                                                 
        p.move_to_relative([-move_distance, 0])
