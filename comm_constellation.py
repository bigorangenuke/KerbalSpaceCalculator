from enum import Enum
import ksp
import numpy as np
import units
class AntennaType(Enum):
    ReflectronDP10 = 0
    Communotron16 = 1

class Antenna():
    def __init__(self,AntType):
        self.type = AntType
        
        rng = [0,2.5e6]
        energy = [0.13]
        
        if self.type == AntennaType.Communotron16:
            rng = [0,2.5e6]
            energy = 0.13 #charge/s
            
        elif self.type ==AntennaType.ReflectronDP10:
            rng = [0,5e5]
            energy = 0.01 #charge/s
        
        self.range = rng
        self.minRange = rng[0]
        self.maxRange = rng[1]
        self.energy = energy



    
    
class Constellation():
    def __init__(self,body, numSat,AntType=1,**kwargs):
        self.body = body
        
        self.numSat = numSat
        self.antType = AntType
        self.ant = Antenna(AntType)
        
        alt = self.satAltitude()
        
        print(alt)
        self.lineOfSight()
        
        if not self.checkLineOfSight():
            print('Constellation() No line of sight')
        else:
            print('has line of sight')
        
    def checkLineOfSight(self):
        if self.lineOfSight()>self.body.radius:
            return True
        
        return False
    
    def estimateDrift(self):
        print('do estimate stuff')
        
    def satAltitude(self):
        return self.body.altitudeForRadius(self.maxRadius())
        
    def lineOfSight(self):
        half_c = self.ant.maxRange * 0.5
        a = self.maxRadius()
        r = np.sqrt(a*a-half_c*half_c)
        return r
        
 
    def maxRadius(self):
      
        c = Antenna(self.antType).maxRange
        
        theta = self.angleBetween()
        
        #law of cosines with a = b
        a = np.sqrt(c*c/(2.*(1.-np.cos(theta))))
        return a
    
    def period(self):
        sma = self.body.radiusForAltitude(self.satAltitude())
        mu = self.body.gravitationalParameter
        return ksp.orbit.orbitalPeriod(sma,mu)
        
    def angleBetween(self,num=None):
        if not num:
            num = self.numSat
        return np.radians(360./float(num))
    
    def distanceBetween(self,alt):
        
        r = self.body.radiusForAltitude(alt)
        
        theta = self.angleBetween()
        
        c = np.sqrt(2*r*r*(1-np.cos(theta)))
        
        print('Satellites are %s m apart at an altitude of %s m'%(c,alt))
        
        return c
        
          

        
        
        
    def __repr__(self):
        mystr = '='*5 + 'COMMUNICATION CONSTELLATION' + '='*5 + '\n'
        mystr += 'Number of Satellites = %s\n'%(self.numSat)
        
        alt = int(self.satAltitude())
        alt = units.cdist(alt,'m','km')
        mystr += 'Altitude = %s km\n'%(alt)
        
        prd = self.period()
        prd = units.ctime(prd,'s','m')
        mystr += 'Period = %s m\n'%(prd)
        mystr += '='*40
        
        return mystr
        
         
  
        
        
if __name__=='__main__':

    kerbin = ksp.Body('kerbin')
    
    sats = Constellation(kerbin,3)
    dx = sats.distanceBetween(750000)
    print(dx)
    dx = units.cdist(dx,'m','km')

    







