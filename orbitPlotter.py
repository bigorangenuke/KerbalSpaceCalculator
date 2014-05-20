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
        r,phi,theta = self.changeOrbitShape()
        x,y,z = crd.sphericalToCartesian(r,phi,theta)
        

        h = self.ecc*np.sin(self.lpe + self.lan)
        k = self.ecc*np.cos(self.lpe + self.lan)
        p = np.tan(self.inc*0.5)*np.sin(self.lan)
        q = np.tan(self.inc*0.5)*np.cos(self.lan)
        
        #meanLongitude = np.arctan(p,q)
    
        #
        return x,y,z
    
    def changeInclination(self,r,theta,dInc):
        print(theta)
        
        
        
    '''  
    def changeOrbitShape(self):
        
        sma = self.sma
        ecc = self.ecc
        inc = np.pi*0.5-self.inc
        
        phi = np.linspace(0,2*np.pi,500)
        r = sma*(1-ecc*ecc)/(1+ecc*np.cos(phi))
        
        theta_dir = np.asarray([0,0,1])
        
        #R = self.orbit.radiusVector()
#         print('======R=======')
#         print(R)
        
        #theta=np.dot(theta_dir,R[0,:])/(np.linalg.norm(R[0,:])*np.linalg.norm(theta_dir))

        theta = np.empty_like(phi)
        
        
        
        
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
        
    '''
        
            
            
        
    
        
        
        