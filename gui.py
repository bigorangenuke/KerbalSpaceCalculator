from PyQt4 import QtGui,QtCore

import os
import numpy as np
from mplwidget import MplWidget as mpl
import matplotlib.pyplot as plt
from PyQt4 import uic
dbg = True

def path_to(file):
    #return absolute path to file
    return os.path.join(os.path.dirname(os.path.abspath(__file__)),file)

def layout_widgets(layout):
    #return iterator of widgets in layout
    return (layout.itemAt(i) for i in range(layout.count))

def removeWidgetsFromLayout(layout):
    #deletes all the widgets in layout
    try:
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().setParent(None)
    except:
        print('gui.removeWidgetsFromLayout() ERROR')
        return False
    return True

class MainWindow(QtGui.QMainWindow):
    def __init__(self,parent=None):
        if dbg: print('MainWindow.__init__()')
        QtGui.QMainWindow.__init__(self,parent)
        #build the .ui file
        uic.loadUi(path_to('mainwindow.ui'), self)
        self.hookupUI()
        #self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    def hookupUI(self):
        if dbg: print('MainWindow.hookupUI()')
        
class GraphWidget(QtGui.QWidget):
    def __init__(self,parent=None):
        if dbg: print('GraphWidget.__init__()')
        QtGui.QWidget.__init__(self,parent)
        uic.loadUi(path_to('graphwidget2.ui'),self)
        self.graph = self.mplwidget
        self.hookupUI()

    def plotOrbit(self,x,y,z=None):
        print('GraphWidget.plotOrbit')
        fig = self.graph.canvas.fig
        ax = fig.add_subplot(111,projection='3d')
        #ax.grid(b=True)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        #ax.view_init(azim = 180+90 , elev = 270)
        ax.plot(x,y,z)
        
  
         
    
        
        
    def hookupUI(self):
        if dbg: print('GraphWidget.hookupUI()')
    

class KSP_GUI():
    def __init__(self,mainwindow):
        self.mainWindow = mainwindow
        self.graphWidget = GraphWidget()
        self.mainWindow.setCentralWidget(self.graphWidget)
        
    
if __name__=='__main__':
    app = QtGui.QApplication([])
    mainWindow = MainWindow()
    gui = KSP_GUI(mainWindow)
    mainWindow.show() 
    
    
    
    #x = np.linspace(1,10,1000)
    #f =( 3*x**(3/2)+2*x)/(2*(x+3)**3+3)
    #plt.plot(x,f)

    app.exec_()
   
        
        
        