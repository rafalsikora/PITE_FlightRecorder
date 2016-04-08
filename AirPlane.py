# This abstract class represents an airplane.

from BlackBox import *
import abc

earthradius = 6371  # km

class AirPlane(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        return

    @abc.abstractmethod
    def fly(self, start, destination):
        return

    # method returning a blackbox object
    def flightdata(self):
        assert isinstance(self.blackbox, BlackBox)
        return self.blackbox.read()
