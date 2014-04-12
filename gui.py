from PyQt4 import QtGui,QtCore

import os
import numpy as np
from mplwidget import MplWidget as mpl
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
        
    def hookupUI(self):
        if dbg: print('MainWindow.hookupUI()')
        
class GraphDockWidget(QtGui.QDockWidget):
    def __init__(self,parent=None):
        if dbg: print('GraphDockWidget.__init__()')
        QtGui.QDockWidget.__init__(self,parent)
        uic.loadUi(path_to('graphwidget.ui'),self)
        self.graph = self.mplwidget
        self.hookupUI()
        
    def hookupUI(self):
        if dbg: print('GraphDockWidget.hookupUI()')
    
def setupMainWindow(mw = None):
    
    graphDockWidget = GraphDockWidget()
    mw.addDockWidget(QtCore.Qt.LeftDockWidgetArea,graphDockWidget)

           
if __name__=='__main__':
    app = QtGui.QApplication([])
    mainWindow = MainWindow()
    setupMainWindow()
    mainWindow.show() 
    
    app.exec_()
   
        
        
        