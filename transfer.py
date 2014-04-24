import ksp
import numpy as np
import ksporbit as orbit
class Transfer():
    def __init__(self,initialOrbit,finalOrbit=None,**kwargs):
        
        if not initialOrbit.__class__== orbit.Orbit().__class__:# or not finalOrbit.__class__==orbit.Orbit().__class__:
            assert False, 'orbit is not of type ksporbit.Orbit()'
    
        self.initialOrbit = initialOrbit
        #self.finalOrbit = finalOrbit
        
        
        
        
        
#     def delta_v(self):
#         
#         st = self.parent.radiusForAltitude(startAltitude)
#         en = self.parent.radiusForAltitude(endAltitude)
#         
#         #semimajor axis of transfer orbit
#         a = (st+en)*0.5
#         
#         #initial velocity at the location of the first impulse
#         v_i1 = np.sqrt(u/st)
#         v_f1 = np.sqrt(u/en)
#         
#         #initial velocity of transfer orbit
#         v_i2 = np.sqrt(u*(2./st - 1./a))
#         #final velocity of transfer orbit (location of  second impulse
#         v_f2 = np.sqrt(u*(2./en-1./a))
#         
#         #delta v for impulse 1
#         dv_a =v_i2-v_i1
#         #delta v for impulse 2
#         dv_b = v_f2-v_f1
# 
#         
#         dv = dv_a + dv_b
#         
#         #super(Transfer,self).__init__(ksp.Body)
#         
#         self.transferType = transferType
#     
# 
#     def hohmannTransfer(self,startAltitude, endAltitude, **kwargs):
#         parent = ksp.Body('kerbin')
#         u = parent.gravitationalParameter
#         if 'parent' in kwargs:
#             parent = kwargs['parent']
#             
#         st = parent.radiusForAltitude(startAltitude)
#         en = parent.radiusForAltitude(endAltitude)
#         
#         #semimajor axis of transfer orbit
#         a = (st+en)*0.5
#         
#         #initial velocity at the location of the first impulse
#         v_i1 = np.sqrt(u/st)
#         v_f1 = np.sqrt(u/en)
#         
#         #initial velocity of transfer orbit
#         v_i2 = np.sqrt(u*(2./st - 1./a))
#         #final velocity of transfer orbit (location of  second impulse
#         v_f2 = np.sqrt(u*(2./en-1./a))
#         
#         #delta v for impulse 1
#         dv_a =v_i2-v_i1
#         #delta v for impulse 2
#         dv_b = v_f2-v_f1
# 
#         
#         dv = dv_a + dv_b
#         return  
            

if __name__ == '__main__':

    o1 = orbit.Orbit(0.1,7500000,0,0,0,0,'earth')
    #o2 = orbit.Orbit(0,900000,0,0,0,0,'kerbin')
    
    nu1  = np.pi/6.
    nu2  = np.pi*0.5
    M1  = o1.meanAnomaly(nu1)
    M2  = o1.meanAnomaly(nu2)
    
    n = o1.meanMotion()
    
    t = (M2-M1)/n
    
    print(M1,M2,t)
     
    #print(p1,p2)
    print(o1.position(0))
    #print(o1.flightPathAngle(np.pi))
    
    transfer = Transfer(o1)
