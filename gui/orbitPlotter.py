import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math as m
import ksp



def generateCoordinates():
    print 'fuck'
    
def coordinatesForOrbit(orbit):
    print 'help'
    e = orbit.eccentricity
    a = orbit.semiMajorAxis
    theta = 0
    
    a = 1.
    e=0
    x=[]
    y=[]
    while theta<=2*m.pi:
        r=(a*(1-e**2))/(1+e*m.cos(theta))
        x.append(r*m.cos(theta))
        y.append(r*m.sin(theta))
        print theta,r
        theta += m.pi/180.
    return x,y
    
kerbin = ksp.Body('kerbin')
x,y=coordinatesForOrbit(kerbin.orbit)
plt.polar(x,y)

plt.show()


# fig = plt.figure()
# ax = fig.add_subplot(111,projection='3d')
# 
# 
# 
# Axes3D.plot()