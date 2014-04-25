import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import jtools
import coordinates as crd

class OrbitPlotter():
    def __init__(self,orbit):
        self.orbit = orbit
        self.ecc = self.orbit.ecc
        self.inc = self.orbit.inc
        self.sma = self.orbit.sma
        self.lpe = self.orbit.lpe
        self.lan = self.orbit.lan
        self.mna = self.orbit.mna
        self.body = self.orbit.body
        
        self.path = None
        
    def getPath(self):
        #x,y= self.orbitShape()
        r,theta,phi = self.changeOrbitShape()
        x,y,z = crd.sphericalToCartesian(r,phi,theta)
        return x,y,z
    
    def changeInclination(self,r,theta,dInc):
        print(theta)
        
    def changeOrbitShape(self):
        
        sma = self.sma
        ecc = self.ecc
        
        phi = np.linspace(0,2*np.pi,2048)
        r = sma*(1-ecc*ecc)/(1+ecc*np.cos(phi))
        theta = np.zeros_like(phi)
        theta.fill(self.inc)
        
        #np.radians(self.inc))
        #r,theta,phi = self.orbitTransform(r,theta,phi, PHI = self.lan)
        #self.orbitTransform(r,theta,phi,'phi'=s)
        #x,y = jtools.polarToRectangular(r,theta)
        return r,phi,theta
    
    def orbitTransform(self,r,phi,theta,**kwargs):
        dr = 0
        dtheta = 0
        dphi = 0
        
        if 'THETA' in kwargs:
            dtheta = kwargs['THETA']
        if 'PHI' in kwargs:
            dphi = kwargs['PHI']
        if 'R' in kwargs:
            dr = kwargs['R']
            
            
        r +=dr
        print('Theta = ',theta)
        theta+=np.radians(dtheta)
        phi += np.radians(dphi)
        
        return r,phi,theta
        
        
        
            
            
        
    
        
        
        