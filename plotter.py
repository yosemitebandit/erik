'''
plotter.py
a plotter lib
origin is top left with positive x 'right' and positive y 'down'
'''
import math
import serial
import sys 
import time


class Plotter:
    def __init__(self, motor_separation, height, motor_radius, serial_path
            , **kwargs):
        # separation between the motor centers (cm)
        self.motor_separation = motor_separation 
        # motors to bottom of canvas (cm)
        self.height = height
        # radius of motor spindle (cm)
        self.motor_radius = motor_radius
        # connect to the serial device
        self.connection = serial.Serial(serial_path, 9600, timeout=1)
        # initialize the pen position (cm)
        self.position = kwargs.pop('initial_position'
            , [motor_separation/2, height/2])
        # set the pen speed (cm/s)
        self.speed = kwargs.pop('speed', 1)


    def move_to_relative(self, offset):
        ''' move by an offset relative to the current position
        '''
        self.move_to([self.position[0]+offset[0], self.position[1]+offset[1]])

    
    def move_to(self, new_position):
        ''' move pen to a new position
        '''
        # calculate the changes in the guidewire lengths
        lengths = self._calculate_guidewire_lengths(self.position)
        new_lengths = self._calculate_guidewire_lengths(new_position)

        # find how much each motor needs to move to achieve the new lengths
        left_steps = self._calculate_steps(lengths[0] - new_lengths[0]) * -1
        right_steps = self._calculate_steps(lengths[1] - new_lengths[1])

        # duration based on length of move and the speed (ms)
        duration = 1000.*math.sqrt((new_position[1] - self.position[1])**2
            + (new_position[0] - self.position[0])**2) / self.speed

        # move the motors
        self.spin_steppers(left_steps, right_steps, duration)
        
        # update the position
        self.position = new_position

        # sleep so the commands don't stack..though stacking's seems to be ok
        time.sleep(duration/1000.)


    def spin_steppers(self, left_steps, right_steps, duration):
        ''' send a command to the steppers
        '''
        command = 'SM,%d,%s,%s\r' % (duration, left_steps, right_steps)
        self.last_command = command
        self.connection.write(command)


    def _calculate_steps(self, guidewire_delta):
        ''' steps the motors will need to move to achieve these deltas
        see readme for details
        3200 steps per revolution in high-res mode
        '''
        return int(1600.*guidewire_delta/(self.motor_radius*math.pi))


    def _calculate_guidewire_lengths(self, position):
        ''' calculate the lengths of the left and right guidewires
        see the readme for details on the trig here
        '''
        return [math.sqrt(position[0]**2 + position[1]**2)
            , math.sqrt((self.motor_separation - position[0])**2
                + position[1]**2)]
