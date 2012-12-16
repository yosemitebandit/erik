## a vertical wall plotter
hang it on your wall, watch it go

![here we are](http://i.imgur.com/toPtD.jpg)


## lib
the small library can output SVG or it can actually drive stepper motors

#### installation
`pip freeze` gave me way too much.  there's really just this lib and pyserial if you don't already have it:

    $ pip install -E /path/to/virtualenv serial
    $ pip install -E /path/to/virtualenv erik

## scripts
there are some scripts inside `bin/` that use the plotting lib

#### emergent-curve
 - draws some straight lines such that they eventually form a curve

#### blocky-spiral
 - drawing a square-shaped spiral starting in the center
 - a labyrinth, I suppose


## plans

### bezier
 - De Casteljau's algorithm is an iterative routine that could be used to turn bezier curves into discrete lines

### portraits
 - maybe this is a shading routine
   - just draw for a while, but avoid regions of low brightness
   - gravitate towards pixels that are darker and in the neighborhood
   - maybe try to stay on a vector
   - how to simulate 'drawing for a while?'


## origins
 - this has been all over the internet for a while
   - see [Harvey Moon's Kickstarter project](http://www.kickstarter.com/projects/notever/the-drawing-machine) for a beautiful example
 - SW rebooted from https://github.com/yosemitebandit/plotplot
 - more technical details on driving the steppers at that repo

