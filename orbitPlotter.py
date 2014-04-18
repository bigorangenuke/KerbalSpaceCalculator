import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math as m

    
class OrbitPlotter():
    def __init__(self,orbit):
        self.orbit = orbit
    
        self.ecc = self.orbit.ecc
