'''
single-curve.py
draw a single bezier curve, mostly for testing
usage, p0 at start; other points described relatively and in quotes
    $ python single-curve.py '3,10 34,8 30,1'
'''
import sys

from bezier import Bezier
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


# capture all the specified control points
# they are relative to the plotter's starting point
specified_control_points = [plotter.initial_position]
for point in sys.argv[1].split(' '):
    specified_control_points.append(
        [plotter.initial_position[0] + float(point.split(',')[0])
        , plotter.initial_position[1] + float(point.split(',')[1])]
    )

if '--control' in sys.argv:
    for point in specified_control_points:
        if point == plotter.initial_position:
            continue
        plotter.move_to(point)
    
    # back to start
    plotter.move_to(plotter.initial_position)


b = Bezier(specified_control_points)
path = b.generate_path()

# plot curve points
for p in path:
    plotter.move_to(p)

# wraps things up with the sim
plotter.finish()
