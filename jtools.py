from numpy import cos,sin,arctan,arccos,sqrt
import numpy

def sphericalToCartesian(*args):
    
    if not len(args)==3:
        print('jtools.sphericalToCartesian not enough args supplied. \n Pass something with length of 3')
        assert(False)
    r,theta,phi = args

        
    x = r*sin(theta)*cos(phi)
    y = r*sin(theta)*sin(phi)
    z = r*cos(theta)
    return [x,y,z]

def cartesianToSpherical(coord):
    x = coord[0]
    y= coord[1]
    z=coord[2]
    
    r = sqrt(x*x+y*y+z*z)
    theta = arccos(z/r)
    phi = arctan(y/x)
    
    return [r,theta,phi]

def polarToRectangular(r,theta):
    return r*cos(theta),r*sin(theta)

def rectangularToPolar(coord):
    x = coord[0]
    y= coord[1]
    return [(x*x+y*y)**(0.5),arctan(y/x)]

def magnitude(vector):
    r=0
    for x in vector:
        r +=x*x
    return r**(0.5)


    