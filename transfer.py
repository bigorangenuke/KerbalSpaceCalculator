import ksp
import numpy as np
import ksporbit as orbit
import units as ut

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
        print(self.initialOrbit)
        self.set_finalOrbit(finalOrbit)
        self.transferTime = 0
        self.burns = []
        self.hohmannTransfer(self.initialOrbit,self.finalOrbit)
        
        self.oneTangentBurnTransfer(self.initialOrbit,self.finalOrbit,28633000)
        
        self.planeChange(np.radians(28),self.initialOrbit)
        ##vf2 = np.sqrt(u*(2./r_f-1./sma_tr))
        #dvi = vi2-vi1
        
    def oneTangentBurnTransfer(self,o1,o2,atx):
        print('start')
        r_a = o1.sma
        r_b = o2.sma
        u = o1.mu
        #Eccentricity
        ecc = 1-(r_a/atx)
        
        #True Anomaly at second burn
        nu = np.arccos((atx*(1.-ecc**2)/r_b-1.)/ecc)
        print('nu = %s'%(nu))
        
        #flight-path angle at second burn
        phi = np.arctan(ecc*np.sin(nu)/(1+ecc*np.cos(nu)))
        
        #initial velocity
        via = np.sqrt(u/r_a)
        vtxa =np.sqrt(u*(2./r_a-1./atx))
        vfb= np.sqrt(u/r_b)
        vtxb = np.sqrt(u*(2./r_b-1./atx))
        
        dva = np.abs(vtxa-via)
        dvb = np.sqrt( vfb**2+vtxb**2-2*vfb*vtxb*np.cos(phi))
        print('flightpathangle = %s'%(phi))
        print('dv_A: %s m/s'%(dva))
        print('dv_B: %s m/s'%(dvb))
        print('dv = %s'%(dva+dvb))
        #eccentric anomaly at B
        E = np.arctan(np.sqrt(1-ecc**2)*np.sin(nu)/(ecc+np.cos(nu)))
        print('E:%s'%(E))
        
        tof = 0.001583913*np.power(atx,1.5)*(E-ecc*np.sin(E))
        print('TOF',ut.ctime(tof,'s','h'))
     
    def hohmannTransfer(self,o1,o2):
        #gravitational parameter
        #Right now, this assumes that remain in 1 sphere of influence
        u =  self.initialOrbit.mu
        
        
        #sma of transfer ellipse
     
        r_a = o1.sma
        print('r_a = ',r_a)
        
        r_b = o2.sma
        print('r_b = ',r_b)


        
        nu = self.initialOrbit.nu

    
        #a_s = initialOrbit.body.altitudeForRadius(r_s)
        #a_f = initialOrbit.body.altitudeForRadius(r_f)
    
        #if dbg: print('transfer.changeAltitude from %s m to %s m. Altitude change: %s'%(a_s,a_f,a_f-a_s))
        
        
        #semimajor axis of transfer orbit
        sma_tr = (r_a+r_b)*0.5
        #eccentricity of transfer orbit
        ecc_tr = orbit.eccentricity(r_a,r_b)
        
        self.transferOrbit= orbit.Orbit(ecc_tr,sma_tr,self.initialOrbit.inc,0,0,0,'earth')
    
        print('ECC: %s\tSMA: %s'%(ecc_tr,sma_tr))
        
        
        T = orbit.orbitalPeriod(sma_tr, u)
        self.transferTime = T*0.5
        print('Time of Transfer = %s h'%(ut.ctime(T*0.5,'s','h')))
        
        via = np.sqrt(u/r_a)
        vfb= np.sqrt(u/r_b)

        vtxa = np.sqrt(u*(2./r_a-1./sma_tr))
        vtxb = np.sqrt(u*(2./r_b-1./sma_tr))
        
        dva = np.abs(vtxa-via)
        dvb = np.abs(vtxb-vfb)
        
        self.burns.append(dva)
        self.burns.append(dvb)
        
        dt = T*0.5
        
        print('dv_A: %s m/s'%(dva))
        print('dv_B: %s m/s'%(dvb))
        
    
    
    
    def planeChange(self,dtheta,o1):
       
        
        v1 = o1.orbitalSpeed(o1.sma)
        dv = 2*v1*np.sin(dtheta*0.5)
        print(dv) 
    
   
        
        
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
#         return  dv
            

if __name__ == '__main__':
    bdy = 'earth'
    
    earth = ksp.Body(bdy)
    radius1 = earth.radiusForAltitude(2e5)
    radius2 = earth.radiusForAltitude(3e5)
    radius1 = 6567000
    radius2 = 42160000
    o1 = orbit.Orbit(0,radius1,0,0,0,0,bdy)
    o2 = orbit.Orbit(0,radius2,0,0,0,0,bdy)
    
    nu1  = np.pi/6.
    nu2  = np.pi*0.5
    
    M1  = o1.meanAnomaly(nu1)
    M2  = o1.meanAnomaly(nu2)
    

    t =Transfer(o1,o2)
    
    o_transfer = t.transferOrbit
    print(o_transfer)


   
     
    #print(p1,p2)
    #print('Position Vector:',o1.position(0))
    #print(o1.flightPathAngle(np.pi))
    
    #transfer = Transfer(o1)
    #dv1 = changeAltitude(o1,1e6)
    
    #print()
