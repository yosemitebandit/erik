'''
emergent-curve.py
draws straight lines between points on the x and y axes to form curves
'''

class Emergent:
    def __init__(self, axis_length, step_size, initial_position, **kwargs):
        self.axis_length = axis_length
        self.step_size = step_size
        self.initial_position = initial_position
        
        quadrant = str(kwargs.pop('quadrant', '1'))
        if quadrant == '1':
            self.direction = [1, 1]
        if quadrant == '2':
            self.direction = [-1, 1]
        elif quadrant == '3':
            self.direction = [-1, -1]
        elif quadrant == '4':
            self.direction = [1, -1]

    def generate_path(self):
        ''' creates an absolute path for the plotter
        '''
        x_axis = self.initial_position[0]
        y_axis = self.initial_position[1]
        x = x_axis
        y = y_axis - self.axis_length * self.direction[1]

        path = []
        while(1):
            path.append([x_axis, y])

            y += self.step_size*self.direction[1]
            path.append([x_axis, y])

            x += self.step_size*self.direction[0]
            path.append([x, y_axis])
            if abs(x - self.initial_position[0]) >= self.axis_length:
                path.append(self.initial_position)
                break

            x += self.step_size*self.direction[0]
            path.append([x, y_axis])
            if abs(x - self.initial_position[0]) >= self.axis_length:
                path.append(self.initial_position)
                break

            y += self.step_size*self.direction[1]

        return path
