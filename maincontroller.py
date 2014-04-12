import gui
import telemachus
import ksporbit as orbit
from PyQt4 import QtGui
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import numpy as np




if __name__=='__main__':
    
    app = QtGui.QApplication([])
    mainWindow = gui.MainWindow()
    gui.setupMainWindow(mainWindow)
    mainWindow.show()
    
    ecc,inc,sma,lan,lpe,mna,bdy = telemachus.read_orbital_elements()
    o = orbit.Orbit(ecc,inc,sma,lan,lpe,mna,bdy)
    

    
    theta = np.linspace(0,2*np.pi,1000)
    r = np.ones_like(theta)
    for i,rr in np.ndenumerate(r):
        r[i] = o.body.radius
    
    x = r*np.cos(theta)
    y = r*np.sin(theta)
    ax = plt.subplot(111)
    #ax.fill_between(x,y)
    plt.plot(x,y)
    x,y = o.calculatePath()
    plt.plot(x,y)
    app.exec_()