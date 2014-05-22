import numpy as np

import telemachus_plugin as tele
import ksp

dbg = False

def orbitalPeriod(sma,mu):
    if dbg: print('ksporbit.orbitalPeriod()')
    assert float(sma) and float(mu)
    return 2*np.pi*np.sqrt(sma**3/mu)

def eccentricity(radius_apo,radius_per):
    assert float(radius_apo) and float(radius_per)
    return np.abs((radius_apo - radius_per))/(radius_apo + radius_per)



class Satellite():
    def __init__(self,orbit,*args,**kwargs):
        
        
        self.orbit = orbit
        
 

        
class Orbit():
    def __init__(self,*args,**kwargs):
        ecc = 0
        sma = 1e6
        inc = 0
        lan = 0
        lpe = 0
        mna = 0
        body = 'kerbin'
        
        nu = 0
        self.r = np.empty(3)
        self.v = np.empty_like(self.r)
        
        self.body=None
        

        if len(args)==0:
            True
        elif len(args)==1:
            arg = args[0]
            if arg.__class__==ksp.Body().__class__:
                self.body = arg  
            elif len(arg)>1:
                ecc = arg[0]
                sma = arg[1]
                inc = arg[2]
                lan = arg[3]
                lpe = arg[4]
                mna = arg[5]
                body = arg[6]
#             elif len(arg)==1:
#                 #Load preset from file
#         
#                 f = open('OrbitalParameters.txt','r')
#                 lines = f.readlines()
#                 f.close()
#                        
#                 for line in lines:
#                     line = [l.strip() for l in line.split(',')] 
#                     row = line
#                     if row[0].lower()==arg.name:
#                         body=str(row[0])
#                         sma=float(row[3])
#                         ecc=float(row[4])
#                         inc=float(row[5])
#                         lpe=float(row[6])
#                         lan=float(row[7])
#                         mna=float(row[8])
#                         #self.periapsis=float(row[11])
#                         #self.periapsisRadius=float(row[10])
#                         #self.apoapsis=float(row[13])
#                         #self.apoapsisRadius=float(row[12])


        elif len(args)==7:
            ecc,sma,inc,lan,lpe,mna,body = args
            if dbg:print(ecc,sma,inc,lan,lpe,mna,body)
        else:
            assert False, 'Bad trouble. Number of args not recognized'
        if not self.body:  
            self.body = ksp.Body(str.lower(body))
        #print(body)
        #print(self.body.radius)
        #print(self.body)
        if 'body' in kwargs:
            self.body = ksp.Body(kwargs['body'])
        mu = self.body.gravitationalParameter
        if 'ecc' in kwargs:
            ecc = kwargs['ecc']
        if 'sma' in kwargs:
            sma = kwargs['sma']
        if 'inc' in kwargs:
            inc = kwargs['inc']
        if 'lan' in kwargs:
            lan = kwargs['lan']
        if 'lpe' in kwargs:
            lpe = kwargs['lpe'] 
        if 'mna' in kwargs:
            mna = kwargs['mna'] 
        if 'mu' in kwargs:
            mu = kwargs['mu']
        if 'nu' in kwargs:
            nu = kwargs['nu']
        
        
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
        
        #gravitational parameter
        self.mu = mu
        #true anomaly
        self.nu = nu
    def __repr__(self):
        elm = dict(self.elements(t = 'dict'))
        str = ''.join(('*'*12,'ORBIT','*'*12,'\n'))
        
        for k,v in elm.items():
            str+='%s:\t%s\n'%(k,v)
        str += '*'*30
        return str
    def elements(self,**kwargs):
        if dbg: print('ksporbit.Orbit.elements()')
        
        
        if 't' in kwargs:
            tkw = kwargs['t']
            if tkw=='dict':
                elm = {}
                elm['ecc'] = self.ecc
                elm['sma'] = self.sma
                elm['inc'] = self.inc
                elm['lan'] = self.lan
                elm['lpe'] = self.lpe
                elm['mna'] = self.mna
                return elm
        
        return self.ecc,self.sma,self.inc,self.lan,self.lpe,self.mna
    
#     def set_apses(self,ap,pe):
#         
        
        
    

    def radiusAtTrueAnomaly(self,nu=None,**kwargs):
        if dbg: print('ksporbit.Orbit.radiusAtTrueAnomaly()')
        if not nu:
            nu = self.nu
        if 'p' in kwargs:
            return kwargs['p']/(1+self.ecc*np.cos(np.radians(nu)))
        
        #TrueAnomaly is angle between position and periapsis
        if dbg:print(self.sma,self.ecc)
        return (self.sma*(1-self.ecc*self.ecc))/(1+self.ecc*np.cos(nu))
    
    def orbitalSpeed(self,r):
        if dbg: print('ksporbit.Orbit.orbitalSpeed()')
        #Vis-viva equation
        #r is the distance between the orbiting bodies
        return np.sqrt(self.mu*(2./r-1./self.sma))
    
    def orbitalPeriod(self):
        if dbg: print('ksporbit.Orbit.orbitalPeriod()')
        return orbitalPeriod(self.sma,self.mu)
    
    def specificOrbitalEnergy(self,r = 0):
        if dbg: print('ksporbit.Orbits,specificOrbitalEnergy()')
        if r:
            v= self.orbitalSpeed(r)
            return v**2/2. - self.mu/r
        else:
            return -self.mu/(2*self.sma)
    
    def specificRelativeAngularMomentum(self):
        if dbg: print('ksporbit.Orbit.specificRelativeAngularMomentum()')
        #need to check if elliptical
        return np.sqrt(self.sma*(1-self.ecc*self.ecc)*self.mu)
    
    def semilatusRectum(self):
        if dbg: print('ksporbit.Orbit.semilatusRectum()')
        #check shape
        return self.smb*self.smb/self.sma
    
    def meanMotion(self):
        if dbg: print('ksporbit.Orbit.meanMotion()')
        mu = self.mu
        if dbg:print(mu)
        return np.sqrt(self.mu/self.sma**3)
    
    def eccentricAnomaly(self,nu):
        if dbg: print('ksporbit.Orbit.eccentricAnomaly()')
        return np.arccos((self.ecc + np.cos(nu))/(1+self.ecc*np.cos(nu)))
    
    def meanAnomaly(self,nu):
        if dbg: print('ksporbit.Orbit.meanAnomaly()')
        E = self.eccentricAnomaly(nu)
        return E - self.ecc*np.sin(E)
    
    def timeOfFlight(self,nu):
        if dbg: print('ksporbit.Orbit.timeOfFlight()')
        return (self.meanAnomaly(nu)-self.mna)/self.meanMotion()
    
#     def position(self,nu):
#         if dbg: print('ksporbit.Orbit.position()')
#         r = self.sma * (1-self.ecc*self.ecc)/(1+self.ecc*np.cos(nu))
#         return r
#     
#     def flightPathAngle(self,nu):
#         if dbg: print('ksporbit.Orbit.flightPathAngle()')
#         phi = np.arctan(self.ecc*np.sin(nu)/(1+self.ecc*np.cos(nu)))
#         return phi

        
        
        
    def azimuthHeading(self):
        if dbg: print('ksporbit.Orbit.azimuthHeading()')
        #cos(i)=cos(delta)*sin(beta)
        if dbg:print('crap')
    
    def geocentricLatitude(self):
        if dbg: print('ksporbit.Orbit.geocentricLatitude()')
        if dbg:print('geocentricLatitude')
    
#     def p(self):
#         return np.tan(self.inc*0.5)*np.sin(self.lan) 
#     
#     def q(self):
#         return np.tan(self.inc*0.5)*np.cos(self.lan)


#     def radiusVector(self,nu=None):
#         nu = np.pi*0.4
#         if not nu:
#             nu = np.linspace(0,2*np.pi,1000)
#             
#         lan = self.lan
#         mna = self.mna
#         i = self.inc
#         
#         #lan = np.pi*0.2
#         #i = 0.0001
#         #mna = 0.001
#         p=self.p()
#         #p =np.tan(i*0.5)*np.sin(lan) 
#         #print(nu)
#         #print(p,lan,mna,i)
#         
#         rx = p*(np.cos(lan)*np.cos(mna+nu)-np.sin(lan)*np.cos(i)*np.sin(mna+nu))
#         ry = p*(np.sin(lan)*np.cos(mna+nu)+np.cos(lan)*np.cos(i)*np.sin(mna+nu))
#         rz = p*np.sin(i)*np.sin(mna+nu)
#         
#         print(rx,ry,rz)
        
        
        
    
        

    


    
    
        
        