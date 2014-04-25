import gui
import telemachus
import ksporbit as orbit
from PyQt4 import QtGui
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import jtools
import numpy as np
import fileman
import orbitPlotter as oplot
import transfer
import ksp
import coordinates as crd
#import orbitPlotter as oplot

if __name__=='__main__':
    
    #Create application instance
    app = QtGui.QApplication([])
    mainWindow = gui.MainWindow()
    kspgui = gui.KSP_GUI(mainWindow)
    mainWindow.show()




    #ecc,inc,sma,lan,lpe,mna,bdy = telemachus.read_orbital_elements()
    #o = orbit.Orbit(ecc,inc,sma,lan,lpe,mna,bdy)
    earth = ksp.Body('earth')
    radius1 = earth.radiusForAltitude(2e5)
    radius2 = earth.radiusForAltitude(3e5)
    
    o1 = orbit.Orbit(0,radius1,0,0,0,0,'earth')
    o2 = orbit.Orbit(0,radius2,0,0,0,0,'earth')
    fig = plt.figure()
    
    phi = np.linspace(0,2*np.pi,5000)
    r = o1.sma*(1-o1.ecc*o1.ecc)/(1+o1.ecc * np.cos(phi))
    theta = np.zeros_like(phi)
    theta.fill(o1.inc)
    
    C = crd.sphericalToCartesian([r,phi,theta])
    X = C[:,0]
    Y = C[:,1]
    Z = C[:,2]
    print(C)
    
    print(X)
    
    
    
#     
#     x = r*np.cos(phi)
#     y = r*np.sin(phi)
#     plt.plot(x,y)
#     plt.show()
#     
    
    
    
    
    
    
    #op = oplot.OrbitPlotter(o1)
    #x,y,z =op.getPath()
    
    
#     
#     t = transfer.Transfer(o1,o2)
#     o3 = t.transferOrbit
# 
#     
#     op =oplot.OrbitPlotter(o1)
#     X,Y,Z=op.getPath()
#     kspgui.graphWidget.plotOrbit(X,Y,Z)
    
    
    
#     orbt = [bdy,ecc,inc,sma,lan,lpe,mna]
#     orbt = [str(x) for x in orbt]
#     fileman.appendFile('orbits.orbit', orbt)
#     
#     op = oplot.OrbitPlotter(o)
#     x,y,z = op.getPath()
#     kspgui.graphWidget.plotOrbit(x,y,z)
#     



#     theta = np.linspace(0,2*np.pi,1000)
#     
#     #Create an empty array to hold calculated radius values
#     r = np.ones_like(theta)
#     print(r[0],theta[0])
#     print(r[0]*np.cos(theta[0]),r[0]*np.sin(theta[1]))
#     #Make a circle of representing kerbin
#     for i,rr in np.ndenumerate(r):
#         r[i] = o.body.radius
#     
# #   #Convert polar to rectangular coordinates
#     x,y = jtools.polarToRectangular(r,theta)
    

    
    

#     ax = plt.subplot(111)
#     #ax.fill_between(x,y)
#     plt.plot(x,y)
#     x,y = o.calculatePath()
#     plt.plot(x,y)

    app.exec_()