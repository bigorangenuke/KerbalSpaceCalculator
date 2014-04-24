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
#import orbitPlotter as oplot

if __name__=='__main__':
    
    #Create application instance
    app = QtGui.QApplication([])
    mainWindow = gui.MainWindow()
    kspgui = gui.KSP_GUI(mainWindow)
    mainWindow.show()

    ecc,inc,sma,lan,lpe,mna,bdy = telemachus.read_orbital_elements()
    o = orbit.Orbit(ecc,inc,sma,lan,lpe,mna,bdy)
    
    orbt = [bdy,ecc,inc,sma,lan,lpe,mna]
    orbt = [str(x) for x in orbt]
    fileman.appendFile('orbits.orbit', orbt)
    
    op = oplot.OrbitPlotter(o)
    x,y,z = op.getPath()
    kspgui.graphWidget.plotOrbit(x,y,z)
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