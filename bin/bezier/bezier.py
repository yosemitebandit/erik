'''
bezier.py
bezier curves via the de Casteljau iterative process
'''
import math

class Bezier:
    def __init__(self, control_points, **kwargs):
        self.control_points = control_points
        self.step_fraction = kwargs.pop('step_fraction', 0.01)
        self.distance_limit = kwargs.pop('distance_limit', 0.01)

    def _find_distance(self, a, b):
        return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

    def _find_angle(self, a, b):
        if a[0] == b[0]:   # bit of a cheat to prevent division by zero
            a[0] += 0.01
        return math.atan((a[1] - b[1]) / (a[0] - b[0]))

    def generate_path(self):
        '''de Casteljau algorithm - iteratively find control points
        each group of control points describes a smaller bezier curve
        hopefully they are small enough that a linear approx is good enough
        '''
        #first set of control points is made up of those specified in input
        control_group = [self.control_points]

        # calculate control points until we go under some distance limit
        k = 0  # kth subsection run
        while(1):
            subsected_points = []
            if k == 0:
                # first run, we'll drop one point in the subsection routine
                iterations = len(control_group[0]) - 1
            else:
                # subsequent runs end with one less point than the original 
                #ctrl points
                iterations = len(control_group[0]) - 1

            for i in range(iterations):
                # find distance between two control points
                distance = self._find_distance(
                    control_group[k][i+1], control_group[k][i])

                # find angle between two control points 
                angle = self._find_angle(
                    control_group[k][i+1], control_group[k][i])
            
                # find_angle uses atan which only returns quadrants I and IV
                # if the vector is in II or III, need to multiply by -1
                if control_group[k][i+1] < control_group[k][i]:
                    forcing = -1
                else:
                    forcing = 1

                # the subsected point is then here:
                subsected_points.append([
                    control_group[k][i][0] + self.step_fraction * distance 
                        * forcing * math.cos(angle)
                    , control_group[k][i][1] + self.step_fraction * distance 
                        * forcing * math.sin(angle)
                ])

            # always hold that last control point
            subsected_points.append(control_group[0][-1])

            if self._find_distance(
                subsected_points[-2], subsected_points[-1]) \
                < self.distance_limit:
                break
            
            k += 1
            control_group.append(subsected_points)

        path = []
        for g in control_group:
            path.append(g[0])
        return path
