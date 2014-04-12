import ksp
import numpy as np

class Transfer():
    def __init__(self,transferType = 1,**kwargs):
        self.initialOrbit = None
        self.finalOrbit = None
        if 'orbit_i' in kwargs:
            assert()
            self.initialOrbit = kwargs['orbit_i']
        
        if 'orbit_f' in kwargs:
            self.finalOrbit = kwargs['orbit_f']
        
        
        
        #super(Transfer,self).__init__(ksp.Body)
        
        self.transferType = transferType
    

    def hohmannTransfer(self,startAltitude, endAltitude, **kwargs):
        parent = ksp.Body('kerbin')
        u = parent.gravitationalParameter
        if 'parent' in kwargs:
            parent = kwargs['parent']
            
        st = parent.radiusForAltitude(startAltitude)
        en = parent.radiusForAltitude(endAltitude)
        
        #semimajor axis of transfer orbit
        a = (st+en)*0.5
        
        #velocity of transfer orbit at peri and apo
        
        v_p = np.sqrt(u * (2./st - 2./(st+en)))
        v_a = np.sqrt(u * (2./en - 2./(st+en)))
        
        dv_p = np.sqrt(u/st)*(np.sqrt(2*en/(st+en))-1)
        dv_a = np.sqrt(u/en)*(1-np.sqrt(2*st/(st+en)))
        dv = dv_p + dv_a
        print(dv)
        return dv   
            

if __name__ == '__main__':
    kerbin = ksp.Body('kerbin')
    transfer = Transfer(kerbin)
