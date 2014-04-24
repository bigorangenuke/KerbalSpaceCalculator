import numpy as np

import telemachus_plugin as tele
import ksp
dbg = True
class Conic():
    def __init__(self):
        self.circle = 0
        self.ellipse = 1
        self.parabola = 2
        self.hyperbola = 3

    
    
        
class Orbit():
    def __init__(self,*args):
        ecc = 0
        sma = 1e6
        inc = 0
        lan = 0
        lpe = 0
        mna = 0
        body = 'kerbin'
        
        if len(args)==0:
            True
        elif len(args)==1:
            
            arg = args[0]

            ecc = arg[0]
            sma = arg[1]
            inc = arg[2]
            lan = arg[3]
            lpe = arg[4]
            mna = arg[5]
            body = arg[6]

        elif len(args)==7:
            ecc,sma,inc,lan,lpe,mna,body = args
            if dbg:print(ecc,sma,inc,lan,lpe,mna,body)
        else:
            assert False, 'Bad trouble. Number of args not recognized'
        self.body = ksp.Body(str.lower(body))
        print(body)
        print(self.body.radius)
        print(self.body)
        
        #Eccentricity (degrees?)
        self.ecc = ecc
        #Semimajor Axis (m)
        self.sma = sma# + self.body.radius
        #Semiminor Axis (m)
        self.smb = sma*np.sqrt(1-ecc*ecc)
        #Inclination (degrees)
        self.inc = inc
        #Right ascension of ascending node,Longitude of Ascending Node (degrees)
        self.lan = lan
        #Argument of periapsis (degrees)
        self.lpe = lpe
        #Mean anomaly at epoch, UT = 0 (radians)
        self.mna = mna
        
        self.mu = self.body.gravitationalParameter
        
    
    def elements(self):
        return self.ecc,self.sma,self.inc,self.lan,self.lpe,self.mna
    
    def calculatePath(self):
        theta = np.linspace(0,2*np.pi,1000)
        r = (self.sma*(1-self.ecc*self.ecc))/(1+self.ecc*np.cos(theta))
        print(self.sma,self.ecc)
        
        x = r*np.cos(theta)
        y = r*np.sin(theta)
        
        return x,y
    
    def radiusAtTrueAnomaly(self,nu,**kwargs):
        if 'p' in kwargs:
            return kwargs['p']/(1+self.ecc*np.cos(np.radians(nu)))
        
        #TrueAnomaly is angle between position and periapsis
        print(self.sma,self.ecc)
        return (self.sma*(1-self.ecc*self.ecc))/(1+self.ecc*np.cos(nu))
    
    def orbitalSpeed(self,r):
        #Vis-viva equation
        #r is the distance between the orbiting bodies
        return np.sqrt(self.mu*(2./r-1./self.sma))
    
    def orbitalPeriod(self):
        return 2*np.pi*np.sqrt(self.sma**3/self.mu)
    
    def specificOrbitalEnergy(self,r = 0):
        if r:
            v= self.orbitalSpeed(r)
            return v**2/2. - self.mu/r
        else:
            return -self.mu/(2*self.sma)
    
    def specificRelativeAngularMomentum(self):
        #need to check if elliptical
        return np.sqrt(self.sma*(1-self.ecc*self.ecc)*self.mu)
    
    def semilatusRectum(self):
        #check shape
        return self.smb*self.smb/self.sma
    
    def meanMotion(self):
        mu = self.mu
        print(mu)
        return np.sqrt(self.mu/self.sma**3)
    
    def eccentricAnomaly(self,nu):
        return np.arccos((self.ecc + np.cos(nu))/(1+self.ecc*np.cos(nu)))
    
    def meanAnomaly(self,nu):
        E = self.eccentricAnomaly(nu)
        return E - self.ecc*np.sin(E)
    
    def timeOfFlight(self,nu):
        return (self.meanAnomaly(nu)-self.mna)/self.meanMotion()
    
    def position(self,nu):
        r = self.sma * (1-self.ecc*self.ecc)/(1+self.ecc*np.cos(nu))
        return r
    
    def flightPathAngle(self,nu):
        phi = np.arctan(self.ecc*np.sin(nu)/(1+self.ecc*np.cos(nu)))
        return phi
    
    def azimuthHeading(self):
        #cos(i)=cos(delta)*sin(beta)
        print('crap')
    
    def geocentricLatitude(self):
        print('geocentricLatitude')
    
    
    
    


    
    
        
        