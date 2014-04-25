import ksp
import numpy as np
import ksporbit as orbit


dbg = True

#def impulse(initialOrbit,endAltitude):
         
def changeAltitude(initialOrbit,finalAltitude):
    if not initialOrbit.__class__== orbit.Orbit().__class__:# or not finalOrbit.__class__==orbit.Orbit().__class__:
        assert False, 'orbit is not of type ksporbit.Orbit()'

    u = initialOrbit.mu
    r_s = initialOrbit.radiusAtTrueAnomaly()
    r_f = initialOrbit.body.radiusForAltitude(finalAltitude)

    a_s = initialOrbit.body.altitudeForRadius(r_s)
    a_f = initialOrbit.body.altitudeForRadius(r_f)

    if dbg: print('transfer.changeAltitude from %s m to %s m. Altitude change: %s'%(a_s,a_f,a_f-a_s))

    #semimajor axis of transfer orbit
    sma_tr = (r_s+r_f)*0.5
    
    vi1 = np.sqrt(u/r_s)
    vf1 = np.sqrt(u/r_f)

    vi2 = np.sqrt(u*(2./r_s-1./sma_tr))
    vf2 = np.sqrt(u*(2./r_f-1./sma_tr))
    dvi = vi2-vi1
    
    


class Transfer():
    def __init__(self,initialOrbit,finalOrbit,**kwargs):
        
        if not initialOrbit.__class__== orbit.Orbit().__class__:# or not finalOrbit.__class__==orbit.Orbit().__class__:
            assert False, 'orbit is not of type ksporbit.Orbit()'
    
        self.initialOrbit = initialOrbit
        
    
        self.set_finalOrbit(finalOrbit)
        
        #gravitational parameter
        #Right now, this assumes that remain in 1 sphere of influence
        u =  self.initialOrbit.mu
        
        r_s = initialOrbit.radiusAtTrueAnomaly()
        
        nu = self.initialOrbit.nu
        #nu = 2
        r_f = self.finalOrbit.radiusAtTrueAnomaly(nu+np.pi*0.5)
    
        #a_s = initialOrbit.body.altitudeForRadius(r_s)
        #a_f = initialOrbit.body.altitudeForRadius(r_f)
    
        #if dbg: print('transfer.changeAltitude from %s m to %s m. Altitude change: %s'%(a_s,a_f,a_f-a_s))
        
        
        #semimajor axis of transfer orbit
        sma_tr = (r_s+r_f)*0.5
        ecc_tr = orbit.eccentricity(r_s,r_f)
        print('Flight Path Angle = ',self.initialOrbit.flightPathAngle(nu))
        self.transferOrbit = orbit.Orbit(ecc_tr,sma_tr,0,0,0,0,'earth')
        
        
        self.transferOrbit.flightPathAngle(2)
        
        
        print('ECC: %s\tSMA: %s'%(ecc_tr,sma_tr))
        
        T = orbit.orbitalPeriod(sma_tr, u)
        
        print('ORBITAL PERIOD = ',T)
        
        vi1 = np.sqrt(u/r_s)
        #vf1 = np.sqrt(u/r_f)
    
        vi2 = np.sqrt(u*(2./r_s-1./sma_tr))
        ##vf2 = np.sqrt(u*(2./r_f-1./sma_tr))
        dvi = vi2-vi1
        
        
        
        
    def set_finalOrbit(self,finalOrbit):
        self.finalOrbit = finalOrbit
        return finalOrbit
        
        
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
    

    def hohmannTransfer(self,startAltitude, endAltitude, **kwargs):
        parent = ksp.Body('kerbin')
        u = parent.gravitationalParameter
        if 'parent' in kwargs:
            parent = kwargs['parent']
            
        st = parent.radiusForAltitude(startAltitude)
        en = parent.radiusForAltitude(endAltitude)
        
        #semimajor axis of transfer orbit
        a = (st+en)*0.5
        
        #initial velocity at the location of the first impulse
        v_i1 = np.sqrt(u/st)
        v_f1 = np.sqrt(u/en)
        
        #initial velocity of transfer orbit
        v_i2 = np.sqrt(u*(2./st - 1./a))
        #final velocity of transfer orbit (location of  second impulse
        v_f2 = np.sqrt(u*(2./en-1./a))
        
        #delta v for impulse 1
        dv_a =v_i2-v_i1
        #delta v for impulse 2
        dv_b = v_f2-v_f1

        
        dv = dv_a + dv_b
        return  dv
            

if __name__ == '__main__':

    earth = ksp.Body('earth')
    radius1 = earth.radiusForAltitude(2e5)
    radius2 = earth.radiusForAltitude(3e5)
    o1 = orbit.Orbit(0,radius1,0,0,0,0,'earth')
    o2 = orbit.Orbit(0,radius2,0,0,0,0,'earth')
    
    nu1  = np.pi/6.
    nu2  = np.pi*0.5
    M1  = o1.meanAnomaly(nu1)
    M2  = o1.meanAnomaly(nu2)

    

    
    o_transfer = orbit.Orbit
    
    t = Transfer(o1,o2)



    
    
    
    n = o1.meanMotion()
    
    t = (M2-M1)/n
    
    print('Mean anomaly at position 1:',M1)
    print('Mean anomaly at position 2:',M2)
    print('Mean motion',n)
    print('Time to move from M1 to M2:',t)
     
    #print(p1,p2)
    print('Position Vector:',o1.position(0))
    #print(o1.flightPathAngle(np.pi))
    
    #transfer = Transfer(o1)
    #dv1 = changeAltitude(o1,1e6)
    
    #print()
