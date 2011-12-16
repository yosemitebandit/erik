import plotter

p = plotter.Plotter(
        # hard to measure solo
        #160.97
        159.5
        # height doesn't really matter
        #, 3*12*2.54
        , 160.97
        # caliper-measured
        , 1.375
        , '/dev/serial/by-id/usb-SchmalzHaus_EiBotBoard-if00')

move_distance = 1
position = p.position

while(1):
    direction = raw_input('specify a direction (udrl): ')                  

    # adjust the desired x,y coordinates of the pen head                   
    if direction == 'u':                                                   
        position = [position[0], position[1]-move_distance]                 
    elif direction == 'd':                                                 
        position = [position[0], position[1]+move_distance]                 
    elif direction == 'r':                                                 
        position = [position[0]+move_distance, position[1]]                 
    elif direction == 'l':                                                 
        position = [position[0]-move_distance, position[1]]                 

    p.move_to(position)

