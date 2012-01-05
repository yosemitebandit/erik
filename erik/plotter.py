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
    def __init__(self, motor_separation, height, motor_radius, **kwargs):
        # separation between the motor centers (cm)
        self.motor_separation = motor_separation 
        # motors to bottom of canvas (cm)
        self.height = height
        # radius of motor spindle (cm)
        self.motor_radius = motor_radius
        # initialize the pen position (cm)
        self.position = kwargs.pop('initial_position'
            , [motor_separation/2, height/2])
        # save this as the starting position as well
        self.initial_position = kwargs.pop('initial_position'
            , [motor_separation/2, height/2])

        # simulated run, rendering svg
        self.simulate = kwargs.pop('simulate', False)
        if self.simulate:
            # initialize the svg path data
            # scaling should be screen's dpi*self.motor_separation
            # scaling is approximate for now
            self.svg_scaling = 10
            # initialize the path with the starting position
            self.simulated_path = 'M%s %s' % \
                tuple([m*self.svg_scaling for m in self.position])
            #self.pixels_per_cm = 3200/(2*math.pi*self.motor_radius)
            self.sim_save_path = kwargs.pop('sim_save_path'
                , 'latest-erik-sim.svg')

        # turning motors, dropping ink
        else:
            # connect to the serial device
            serial_path = kwargs.pop('serial_path', None)
            self.connection = serial.Serial(serial_path, 9600, timeout=1)
            # set the pen speed (cm/s)
            self.speed = kwargs.pop('speed', 1)
            # do not print commands sent to the board by default
            self.verbose_commands = kwargs.pop('verbose_commands', False)


    def finish(self):
        ''' finish and save the simulation
        could maybe move the pen back to some starting point one day
        or add a signature, hah
        '''
        if self.simulate:
            svg_contents = '''
                <svg
                    version="1.1"
                    baseProfile="full" 
                    xmlns="http://www.w3.org/2000/svg"
                    width="%spx"
                    height="%spx"
                >
                <path d='%s' stroke='blue' fill='transparent' />
                </svg>
            ''' % (self.motor_separation*self.svg_scaling \
                    , self.height*self.svg_scaling \
                    , self.simulated_path)

            # save the svg
            f = open(self.sim_save_path, 'w')
            f.write(svg_contents)
            f.close()


    def move_to_relative(self, offset):
        ''' move by an offset relative to the current position
        '''
        self.move_to([self.position[0]+offset[0], self.position[1]+offset[1]])
    
    
    def move_to_relative_to_start(self, offset):
        ''' move by an offset relative to the starting position
        '''
        self.move_to([self.initial_position[0]+offset[0]
            , self.initial_position[1]+offset[1]])

    
    def move_to(self, new_position):
        ''' move pen to a new position
        or build the simulated svg path 
        '''
        if self.simulate:
            self.simulated_path += 'L%s %s' % \
                tuple([m*10 for m in new_position])
        
        else:
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
            
            # sleep so the commands don't stack..though stacking's seems to be ok
            time.sleep(duration/1000.)
        
        # update the position
        self.position = new_position


    def spin_steppers(self, left_steps, right_steps, duration):
        ''' send a command to the steppers
        '''
        command = 'SM,%d,%s,%s\r' % (duration, left_steps, right_steps)
        if self.verbose_commands:
            print command
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
