#!/usr/bin/env python
import random
import time

import envoy

'''
sizes on [5, 15]
spacing on [0.15, 0.3]
angle on [10, 110]
distance [3, 30]

direction chosen by even-out algo
direction [u, l, d, r]
'''

x_sum = 0
y_sum = 0 

while(1):
    # shape starting point
    distance = int(random.random()*21 + 3)
    if x_sum > 0:
        direction = 'l'
        x_sum -= distance
    else:
        direction = 'r'
        x_sum += distance
    envoy.run('python /home/matt/erik/bin/move-self.py %s %s' % (distance, direction))
    print 'x: '
    print distance, x_sum

    distance = int(random.random()*21 + 3)
    if y_sum > 0:
        direction = 'd'
        y_sum -= distance
    else:
        direction = 'u'
        y_sum += distance
    envoy.run('python /home/matt/erik/bin/move-self.py %s %s' % (distance, direction))
    print 'y: '
    print distance, y_sum

    # flutterby params
    size = int(random.random()*10 + 5)
    spacing = round(random.random()*.15 + 0.15, 2)
    angle = int(random.random()*100 + 10)

    print size, spacing, angle 
    envoy.run('python /home/matt/erik/bin/emergent-curve/flutterby.py %s %s %s' % (size, spacing, angle))
