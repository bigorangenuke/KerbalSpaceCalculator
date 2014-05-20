
import ksporbit as orbit
import numpy.log as ln

class Satellite():
    def __init__(self,position):
        
        #position vector
        self.p = position
        
        #velocity vector
        self.v =None
        
class Vessel():
    def __init__(self,position):
        self.stages = 1
        
        #Mass will be of length stages
        #Each entry will contain wet mass and dry mass
        self.mass=[]
        
class Stage():
    def __init__(self):
        self.wet_mass = 0
        self.dry_mass = 0
        
        self.liquid_fuel = 0
        self.oxidizer = 0
        
        self.specific_impulse = 0
    

def deltaV(wet_mass,dry_mass,specific_impulse,standard_gravity):
    
    i_sp = specific_impulse
    g_0 = standard_gravity
    v_e = i_sp*g_0
    
    delta_v = v_e*ln(wet_mass/dry_mass)
    return delta_v
        
        
        #orbit.elementsForVectors(self.p,self.v)
        