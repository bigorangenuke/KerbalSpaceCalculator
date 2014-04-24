import math as m
import numpy as np
import csv



#import sympy as sp


G = 6.67384e-11 #m^3/kg/s^2
dbg = True
ksp =True



class Body():
    def __init__(self,bodyName=None):
        if not bodyName:
            bodyName = 'kerbin'
            
        self.name=None
        self.referenceCode=None
        self.parent=None
        self.radius=None#meters
        self.gravitationalParameter=None#m^3/s^2
        self.sphereOfInfluence=None#meters
        self.siderealDay=None#seconds
        self.hasAtmosphere=False
        self.hasOxygen=False
        self.pressureAtSeaLevel=None#dunno
        self.atmosphereScaleHeight=None#dunno
        self.atmosphereCutoff=None #km
        self.hasOceans= False
        self.orbit = None
        
        self.importDataForBody(bodyName)
        
        
    def __str__(self):
        return self.name
    
    def surfaceGravity(self):
        f = self.forceOfGravity(0)
        if dbg: 'surface gravity = ', f,'m/s**2'
        return f
    
    def forceOfGravity(self,altitude,mass=None):
        
        r = self.radius+altitude
        
        if not mass:
            mass = 1 #kg
    
        force = self.gravitationalParameter*mass/r/r
        if dbg: 'Force of gravity = ', force, 'N'
        return force  
    
    def synchronousOrbit(self,radius=False):
        so = pow(self.gravitationalParameter*(self.siderealDay/(2.*m.pi))**2,(1./3.))
        print (self.gravitationalParameter,self.siderealDay)
        
        if not ksp:
            if radius:
                return so
            else:
                return self.altitudeForRadius(so)
            
        if so>self.sphereOfInfluence:
            return 0
        else:
            if radius:
                return so
            else:
                return self.altitudeForRadius(so)
            
    def semiMajorAxisForOrbitalPeriod(self,orbitalPeriod):
        sma = pow(self.gravitationalParameter*(orbitalPeriod/2./m.pi)**2,1./3.)
        return sma      
    
    def escapeVelocity(self,r=None):
        if not r: r = 0
        ra = self.radiusForAltitude(r)
        ev =m.sqrt(2*self.gravitationalParameter/ra)
        if dbg: print ('escape velocity = ', ev, 'm/s')
        return ev
    
    def radiusForAltitude(self,altitude):
        print (self.radius, altitude)
        return self.radius+altitude
    
    def altitudeForRadius(self,radius):
        return radius-self.radius
    
    def mass(self):
        return self.gravitationalParameter/G
        
    def importDataForBody(self,body):
        with open('PhysicalParameters.txt') as f:
            if dbg: 'ksp.Body.importDataForBody'
            reader = csv.reader(f)
            for row in reader:
                if row[0].lower()==body:
                    if dbg: print (row[0])
                    self.name=body
                    self.referenceCode=int(row[1])
                    if row[2]:
                        self.parent=Body(row[2].lower())
                    self.radius=float(row[3])#meters
                    self.gravitationalParameter=float(row[4])#m^3/s^2
                    self.sphereOfInfluence=float(row[5])#meters
                    self.siderealDay=float(row[6])#seconds
                    if row[8]:
                        self.hasAtmosphere=True
                        if row[7]=='Oxygen':
                            self.hasOxygen=True
                        else:
                            self.hasOxygen=False
                        self.pressureAtSeaLevel=float(row[8])#dunno
                        self.atmosphereScaleHeight=int(row[9])#dunno
                        self.atmosphereCutoff=float(row[10]) #km
                    else:
                        self.hasAtmosphere=False
                            
                    if row[11]=="Yes":
                        self.hasOceans=True
                    else:
                        self.hasOceans=False
                        
                    self.orbit = Orbit(self)
            f.close()
        print()
        
        
class Orbit():
    def __init__(self,body,isArtificial=None):
        self.body = body
        self.parent = None
        self.semiMajorAxis=None
        self.eccentricity=None
        self.inclination=None
        self.argumentOfThePeriapsis=None
        self.longitudeOfTheAscendingNode=None
        #Mean Anomaly at epoch UT = 0.0 (in radians)
        self.meanAnomaly=None
        self.periapsis=None
        self.periapsisRadius=None
        self.apoapsis=None
        self.apoapsisRadius=None
        
        if isArtificial:
            print('satellite')
            self.parent =  body
        else:
            #Load preset from file
            if body.name:
                with open('OrbitalParameters.txt') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        if row[0].lower()==body.name:
                            self.body = body
                            self.parent = body.parent
                            self.semiMajorAxis=float(row[3])
                            self.eccentricity=float(row[4])
                            self.inclination=float(row[5])
                            self.argumentOfThePeriapsis=float(row[6])
                            self.longitudeOfTheAscendingNode=float(row[7])
                            self.meanAnomaly=float(row[8])
                            self.periapsis=float(row[11])
                            self.periapsisRadius=float(row[10])
                            self.apoapsis=float(row[13])
                            self.apoapsisRadius=float(row[12])
                    f.close()

    def specificAngularMomentum(self):
        #http://en.wikipedia.org/wiki/Specific_angular_momentum#Elliptical_orbit
        b = self.semiMinorAxis()
        a = self.semiMajorAxis
        u = self.body.gravitationalParameter
        m1 = self.parent.mass()
        m2 = self.body.mass()
        h= 2*m.pi*a*b/(2*m.pi*m.sqrt(a*a*a/(G*(m1+m2))))
        if dbg: print ("specific angular momentum = ", h)
        return h
    
    def semiMinorAxis(self,eccentricity=None,semimajorAxis=None):
        ecc = self.eccentricity
        a = self.semiMajorAxis
        if eccentricity:
            ecc = eccentricity
        if semimajorAxis:
            a = semimajorAxis
        b = a*m.sqrt(1-ecc**2)
        if dbg:print ('Semi-Minor Axis = ', b,"m")
        return b
        
    def orbitalPeriod(self,*semimajorAxis, **gravitationalParameter):
        
        u =self.body.gravitationalParameter
        if self.semiMajorAxis:
            a = self.semiMajorAxis
        
        if semimajorAxis:
            a = semimajorAxis
            
    
        if gravitationalParameter:
            u = gravitationalParameter
        period = m.sqrt(4*m.pi*m.pi*a**3/u)
        if dbg: print ("period = ", period ,"s")
        return period
        
    def gm(self,m1=None,m2=None):
        m = self.body.mass()
        M = self.parent.mass()
        if m1:
            m = m1
        if m2:
            M=m2
        return G*(M+m)
    
    def altitudeForOrbitalPeriod(self,period,gravitationalParameter=None):
        if not gravitationalParameter:
            gravitationalParameter=self.body.gravitationalParamter
        r = m.pow(period*period*gravitationalParameter/(4*m.pi*m.pi),(1/3.))
        if dbg: print ('Altitude of',r, 'm required for orbital period of', period,'s')
        
                             
    def orbitalSpeed(self,altitude,radius=None,gravitationalParameter=None):
        
        u=self.parent.gravitationalParameter
        r = self.parent.radiusForAltitude(altitude)
        print(r)
        if r>self.apoapsisRadius or r<self.periapsisRadius:
            print ('Orbt.orbitalSpeed altitude is greater than periapsis/apoapsis')
        #self.orbitalSpeed = m.sqrt(u*(2/r-1/self.semiMajorAxis))
        
        if radius:
            r = radius + altitude
        if gravitationalParameter:
          
            u = gravitationalParameter
            
        v =  m.sqrt(u/r)
 
        if dbg: print ('Orbital Speed =', v,'m/s')
        return v
            
    def specificOrbitalEnergy(self):
        #Joules per kilogram
        u=self.body.gravitationalParameter
        a = self.semiMajorAxis
        return -u/2./a



    

def interplanetaryHohmannTransfer(originAltitude,originBody,targetBody):
    print ('*'*25)
    print ('Hohmann Transfer from', originBody.name.capitalize(), '(',originAltitude,'m ) to ',targetBody.name.capitalize())
    r1 = originBody.orbit.periapsisRadius
    r2 = targetBody.orbit.periapsisRadius
    alt = originBody.radiusForAltitude(originAltitude)
    u = sun.gravitationalParameter    
    oSoi = originBody.sphereOfInfluence
    ou = originBody.gravitationalParameter
    
    r1 = 13.5e6
    r2 = r1*3
    alt = 700e3
    oSoi = 82e6
    u = 1.167922e9
    ou=3530.461

  
    
    time = m.pi*m.sqrt((r1+r2)**3/(8.*u))
    print ('Transfer Time =',time,'s')
    ev = originBody.escapeVelocity()
    
   
    print ("Escape velocity = ",ev,'m/s')
    targetTravel = m.sqrt(u/r2)*time/r2*180/m.pi
    phaseAngle=180-targetTravel
    
    print ('Kerbin r =', r1, 'm\tDuna r =',r2,'m')
    
    print ('Phase Angle (in degrees) = ', phaseAngle)

    
    velocityAtEdgeOfSoi = m.sqrt(u/r1)*(m.sqrt(2*r2/(r1+r2))-1)
    v2 = velocityAtEdgeOfSoi
    
    ejectionVelocity = m.sqrt((alt*(oSoi*v2*v2-2*ou)+2*oSoi*ou)/(alt*oSoi))
    print ("ejection velocity = ", ejectionVelocity ,"m/s")
    
    specificOrbitalEnergy = ejectionVelocity**2/2-ou/alt
    h = ejectionVelocity*alt
    ee = m.sqrt(1+2*epsilon*h*h/ou/ou)
    ejectionAngle = 180-m.acos(1/ee)
    
    print ('ejection angle (in degrees) =',ejectionAngle)
   
    
class Satellite():
    def __init__(self,parent,mass):
        self.mass=mass
        self.altitude = None
        self.parent=parent
        
        self.mass = None
        #self.orbit = Orbit(earth,True)

        
        
        
if __name__ == '__main__':
    
    kerbin = Body('kerbin')
    hohmannTransfer(1e5,2e5)
#sun = Body('sun')
# kerbin = Body('kerbin')
# duna = Body('duna')
# 
# earth = Body('earth')
# sat = Satellite(earth,1)
# sat.altitude=200000
# sat.orbit.orbitalSpeed(sat.altitude)
# 
# print '*'*20
# 
# 
# if dbg: 'Problem 1 = ', sat.orbit.orbitalSpeed(sat.altitude),'m/s'
# if dbg: 'Problem 2 = ', sat.orbit.orbitalPeriod(sat.altitude),"s"
# 



