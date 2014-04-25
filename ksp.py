import math as m
import numpy as np
import csv
import ksporbit as orbit


#import sympy as sp


G = 6.67384e-11 #m^3/kg/s^2
dbg = False
ksp =True



class Body():
    def __init__(self,bodyName=None):
        doImportData = True
        if not bodyName:
            doImportData = False
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
        self.pressureAtSeaLevel=None#kPa
        self.atmosphereScaleHeight=None#dunno
        self.atmosphereCutoff=None #km
        self.hasOceans= False
        self.orbit = None
        
        if doImportData:
            self.importDataForBody(bodyName)
        
        
    def __str__(self):
        return self.name
    
    def surfaceGravity(self):
        f = self.forceOfGravity(0)
        if dbg: 'surface gravity = ', f,'m/s**2'
        return f
    
    def forceOfGravity(self,altitude,mass=None):
        if dbg: print('ksp.Body.forceOfGravity()')
        r = self.radius+altitude
        
        if not mass:
            mass = 1 #kg
    
        force = self.gravitationalParameter*mass/r/r
        if dbg: 'Force of gravity = ', force, 'N'
        return force  
    
    def synchronousOrbit(self,radius=False):
        if dbg: print('ksp.Body.synchronousOrbit()')
        so = pow(self.gravitationalParameter*(self.siderealDay/(2.*m.pi))**2,(1./3.))
       
        
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
        if dbg: print('ksp.Body.semiMajorAxisForOrbitalPeriod()')
        sma = pow(self.gravitationalParameter*(orbitalPeriod/2./m.pi)**2,1./3.)
        return sma      
    
    def escapeVelocity(self,r=None):
        if dbg: print('ksp.Body.escapeVelocity()')
        if not r: r = 0
        ra = self.radiusForAltitude(r)
        ev =m.sqrt(2*self.gravitationalParameter/ra)
        if dbg: print ('escape velocity = ', ev, 'm/s')
        return ev
    
    def radiusForAltitude(self,altitude):
        if dbg: print('ksp.Body.radiusForAltitude()')
        #print (self.radius, altitude)
        return self.radius+altitude
    
    def altitudeForRadius(self,radius):
        if dbg: print('ksp.Body.altitudeForRadius()')
        return radius-self.radius
    
    def mass(self):
        if dbg: print('ksp.Body.mass()')
        return self.gravitationalParameter/G
        
    def importDataForBody(self,body):
        if dbg: print('ksp.Body.importDataForBody(%s)'%(body))
        filename = 'PhysicalParameters.txt'

        f= open(filename,'r')
        lines = f.readlines()
        f.close()

        bodyFound = False
        for line in lines:
            if dbg: 'ksp.Body.importDataForBody'
            line = [l.strip() for l in line.split(',')]
            row = line
            if row[0].lower()==body:
                bodyFound = True
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
                    
                self.orbit = orbit.Orbit(self)
                
        assert bodyFound,'body %s not found in %s'%(body,filename)


