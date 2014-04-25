import ksp
import math as m
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import jmath

dbg = True

class Satellite():
    def __init__(self,parent,mass):
        self.mass=mass
        self.body = parent
        self.mass = None
        self.orbit = Orbit(self,self.body)
        self.position=[]
        self.velocity=[]
        self.time =0
        
    def set_position(self,pos):
        pol = jmath.rectangularToPolar(pos)
        pol[0]+=self.body.radius
        self.position = jmath.polarToRectangular(pol)
    
    def step(self):

        p =self.position
        v = self.velocity
        dt = 2
        pos = []
        vel = []
        
     
        dv = self.orbit.getAcceleration(self.body.gravitationalParameter/self.body.mass(),self.mass,p,v)*dt
        v = v+dv*dt
        p = p+v*dt
        print p
        self.position = p
        self.time+=dt

        return p

    
class Orbit():
    def __init__(self,satellite,body):
        self.satellite = satellite
        self.body = body
        self.altitude = None
        self.semiMajorAxis=None
      
        self.periapsis=None
        self.periapsisRadius=None
        self.apoapsis=None
        self.apoapsisRadius=None
        
        self.inclination=None
        self.argumentOfThePeriapsis=None
        self.longitudeOfTheAscendingNode=None
        self.meanAnomaly=None
        self.time =0
        
        
    def radius(self,altitude=None):
        a = self.altitude
        if altitude:
            a = altitude
        return self.body.radius + a
    
    def orbitalSpeed(self,altitude=None):
        r = self.radius()
        if altitude:
            r = self.radius(altitude)
        u = self.body.gravitationalParameter
        v = m.sqrt(u/r)
        
        return v
        
    def orbitalPeriod(self,**kwargs):
        a = None
        u = self.body.gravitationalParameter
        
        if self.semiMajorAxis:
            a = self.semiMajorAxis
        else:
            a = self.radius()
    
        if kwargs:
            print 'kwargs passed'
            if 'SMA' in kwargs:
                a = kwargs['sma']
            if 'mu' in kwargs:
                u = kwargs['mu']
        
    
        period = m.sqrt(4*m.pi*m.pi*a**3/u)
        
        if dbg: print "period = ", period ,"s"
        return period
    
    def radiusForPeriod(self,period):
        d = self.body.gravitationalParameter*period*period/(4*m.pi*m.pi)
    
        a = pow(d,1./3.)
        return a
    def set_apoapsis(self,ap):
        self.apoapsis=ap
        self.apoapsisRadius=self.radius(ap)
        
    def set_periapsis(self,pe):
        self.periapsis=pe
        self.periapsisRadius=self.radius(pe)
    def eccentricity(self):
        a = self.apoapsisRadius
        p = self.periapsisRadius
        
        return (a-p)/(a+p)
    
    def path(self):
        print '*'*20
        ap = self.apoapsisRadius
        #ap = self.apoapsis
        pe = self.periapsisRadius
        #pe = self.periapsis
        u = self.body.gravitationalParameter
        e = self.eccentricity()
        
        #print u,e
        print "(",pe,",", ap,")"
        
        i = np.radians(self.inclination)
        print self.inclination,i
        
        sma = (ap + pe) * 0.5
        
        
        theta = np.linspace(0,2*m.pi,360*2)
        
        #calculate orbit
        r = sma*(1-e*e)/(1+e*np.cos(theta))
        
        x = r*np.sin(theta)*np.cos(i)
        y = r*np.sin(theta)*np.sin(i)
        #z =np.zeros(x.size)
        
        z = r*np.cos(theta)
        
        for j in range (0,x.size-1):
            print x[j],y[j],z[j]
            
        #print x,y,z
        return x,y,z
        
    def referencePlane(self):
        v = self.radius(500000)
        sma = (v+v) * 0.5
        e = 0
        theta = np.linspace(0,2*m.pi,360)
        r = sma*(1-e*e)/(1+e*np.cos(theta))
        
        
        return x,y,z


        
        
    def simulate(self):
        sat = self.satellite
        p = sat.position
        pol = jmath.rectangularToPolar(p)
       
        pol[0]+=self.body.radius
        p = jmath.polarToRectangular(pol)
        
        #sph[0]+= self.body.radius
        #p = jmath.sphericalToCartesian(sph)
        

        v = sat.velocity
        g = sat.body.gravitationalParameter/sat.body.mass()
        
    
        #print p,v
    
        
        i = 0
        dt = 1
        iterations = 100000
        pos = []
        vel=[]
        t = 0
        while i<iterations: 
            dv = self.getAcceleration(g,sat.mass,p,v)*dt
            #print dv
            v = v+dv*dt
            p = p+v*dt
            t+=dt
            #print p,v,dv
            pos.append(p)
            vel.append(v)
            i+=1
        
        x,y=[],[]
        [x.append(a[0]) for a in pos]
        [y.append(a[1]) for a in pos]  
        fig = plt.figure(figsize=(5,10))
        plt.subplot(211)
        plt.plot(x,y)
        
        u,w=[],[]
        [u.append(vv[0])for vv in vel]
        [w.append(vv[1]) for vv in vel]
        plt.subplot(212)
        plt.plot(u,w)
        
        
        plt.show()
    
    def getAcceleration(self,g,m,p,v):
        u = self.body.gravitationalParameter
        r = 0
        for x in p: 
            r +=x*x
        r = r**(0.5)
        #print r
        
        vm=jmath.magnitude(v)
        
        #dv = r*g*m
        dv = u/r/r
    
        
        
        a=np.empty((2))
#         a[0]=-v[1]/float(vm)*dv
#         a[1]=v[0]/float(vm)*dv
        a[0]=-p[0]/r*dv
        a[1]=-p[1]/r*dv
        #print a
        return a
        
        
   
    
    
    






# ap = sp.Symbol('ap')
# pe = kerbin.radiusForAltitude(100000)

# maxRange=5e6
# p=1e5
# goal = 3e6

# while True:
#     pe = kerbin.radiusForAltitude(p)
#     roots =sp.solve((1+(ap-pe)/(ap+pe))*sma-ap,ap)
#     
#     if roots[1]<goal:
#         print '*' * 20
#         print p, roots[1]
#         break
#     else: p +=10000


# v = sat.orbit.orbitalSpeed()
# print "Problem 1: ",v, "m/s"
# t = sat.orbit.orbitalPeriod()
# print "Problem 2: ",t, "s"
# 
# 
# gst = sat.body.siderealDay
# 
# r = sat.orbit.radiusForPeriod(gst)
# 
# print "Problem 3: ",r,"m"
# 
# t=sat.orbit.set_apoapsis(2000000)
# t=sat.orbit.set_periapsis(200000)
# t=sat.orbit.inclination = 45 #degrees
# 
# 
# x,y,z=sat.orbit.path()
# fig = plt.figure(figsize = plt.figaspect(1))
# ax=fig.add_subplot(111,projection='3d')
# ax.plot(x,y,z)
# 
# sat.orbit.inclination = 20
# 
# a,b,c = sat.orbit.path()
# ax.plot(a,b,c)
# 
# plt.show()




