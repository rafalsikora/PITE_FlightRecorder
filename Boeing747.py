# This class represents Boeing 747 aircraft (subclass of AirPlane)

from AirPlane import *
from numpy import *
from random import *


class Boeing747(AirPlane):

    def __init__(self):
        super(AirPlane, self).__init__()
        self.blackbox = BlackBox()
        self.distanceerror = 0.2  # kilometers
        self.timestep = 1  # seconds
        self.normalaltitude = 35000  # feet
        self.climbrate = 15  # feet per second
        self.parameterchangeprobability = 0.1  # per second
        self.vmax = 0.2  #km/s

    # method simulating a full flight, basically a time loop with step equal self.timestep
    def fly(self, start, destination):
        time = 0
        currentposition = [start[0], start[1], start[2]]
        height = 0
        direction = [destination[0]-start[0], destination[1]-start[1], destination[2]-start[2]]
        distance = sqrt(direction[0]**2+direction[1]**2) * earthradius
        direction /= sqrt(direction[0]**2+direction[1]**2)
        pitch = 0
        roll = 0
        while distance > self.distanceerror:
            time += self.timestep
            if height < self.normalaltitude*0.3:
                vz = self.climbrate*0.3
                v = 0.3*self.vmax
            else:
                vz = uniform(-3, 3)
                v = self.vmax
            if random() < self.parameterchangeprobability*self.timestep:
                pitch += uniform(-0.1, 0.1)
            if random() < self.parameterchangeprobability*self.timestep:
                roll += uniform(-0.1, 0.1)
            vx = v*direction[0]
            vy = v*direction[1]
            height += self.timestep * vz
            currentposition[0] += vx*self.timestep/(earthradius+height*0.3)
            currentposition[1] += vy*self.timestep/(earthradius+height*0.3)
            direction = [destination[0]-currentposition[0], destination[1]-currentposition[1],
                         destination[2]-currentposition[2]]
            distance = sqrt(direction[0]**2+direction[1]**2) * earthradius
            direction /= sqrt(direction[0]**2+direction[1]**2)
            # saving data from sensors to black-box
            self.blackbox.save({"phi": currentposition[0],
                                "lambda": currentposition[1],
                                "alt": height,
                                "pitch": pitch,
                                "roll": roll,
                                "time": time})
