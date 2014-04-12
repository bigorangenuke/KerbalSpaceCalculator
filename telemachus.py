import telemachus_plugin as tele

def read_orbital_elements():
    
    ecc=0
    inc=0
    sma=0
    bdy=None
    lan=0
    lpe=0
    mna=0
    try:
        ecc =tele.read_eccentricity()
        inc = tele.read_inclination()
        
        
        per = tele.read_periapsis()
        apo = tele.read_apoapsis()
        
        sma = per/(1.-ecc*ecc)
        bdy = tele.read_body()
        
    
    
        lan = tele.read_longitudeOfAscendingNode()
        lpe = tele.read_argumentOfPeriapsis()
        mna = tele.read_meanAnomalyAtEpoch()
        
        trueanomaly = tele.read_trueAnomaly()
        print(trueanomaly)
    
        print ("ECC",ecc)
        print ("INC",inc)
        print("SMA",sma)
        print("LAN",lan)
        print("LPE",lpe)
        print("MNA",mna)
        print('Body',bdy)
        
    except:
        print('ERROR Exception when accessing telemachus api')
    try:
        mu = tele.read_bodyGravitationalParameter()
        print('Mu',mu)
    except:
        print('Error accessing body gravitational parameter')
    
    return ecc,sma,inc,lan,lpe,mna,bdy

    

