#Parsing parts files
import os
pfn = 'F://Games//KMP//Squad//Parts//FuelTank'


from enum import Enum

def readPartFile(partFile):
    #print(partFile)
    f = open(partFile, 'r')
    lines = f.readlines()
    f.close()
    lines = [line.strip() for line in lines if line != '\n']
    for i,line in enumerate(lines):
        if '=' in line:
            lines[i] = line.split('=')
    
    lines = [line for line in lines if line]
    print(lines)
    
    startlines = st = [i for i,line in enumerate(lines) if '{' in line]
    
    for ln in startlines:
        if '{' in lines[ln]:
            print(ln)
    
    
    endlines = en = [i for i,line in enumerate(lines) if '}' in line]
    
    assert len(startlines)==len(endlines),'File incomplete'

    #Add the lists together
    dl = st+en
    
    #O
    modlst = []

    x = 0
    
    #===========================================================================
    # When the index comes from start positions, a new list object is added to 
    #     modlst with a zero in place of the last item.
    # When the index comes from an end position, it walks backwards up the 
    #     modlst until it find a list that has a zero in the last item
    # This value is accepted and set to the last item of current list in modlst
    #===========================================================================
    for d in dl:
        #print(d)
        #print (lst)
        if d in st: 
            x+=1
            modlst.append([d,0])
            
        if d in en:
            i = 0
            x-=1
            for i in reversed(range(len(modlst))):
                ck = modlst[-i]
                i+=1 
                if ck[-1]==0:
                    ck[-1] = d
                    #print(ck)
                    #print(ck)
                    break
  

    #===========================================================================
    # Slice lines with bounds in modlst
    #===========================================================================
    mods = []
    for m in modlst:
        a = m[0]
        b = m[1]
        #print(lines[a-1])
        #print(lines[b])
        
        
        mln = lines[a-1:b+1]
        
        
        print('a,b = ',a,b)
 
        print('LINES:\t',lines[a-1],lines[a],lines[b],lines[b])
        #print(a -1,b+1)
        #print(mln)
        
        mt = mln[0].strip()
        
        #print('MODULE TYPE =',mt)
        moduleType=None
        
        
        
        
        #print(a,b)
        nm = None
        if mt =='PART':
            moduleType = ModuleType.PART
            nm = Part(mln,ix = m)
        elif mt=='RESOURCE':
            moduleType = ModuleType.RESOURCE
            nm = Resource(mln,ix = m)
        elif mt=='PROPELLANT':
            nm = Propellant(mln,ix = m)
            moduleType = ModuleType.PROPELLANT
        elif mt=='MODULE':
            moduleType = ModuleType.MODULE
            nm = Module(mln,ix=m)
        else:
            assert False,'Module type not recognized'
        
        
        

        mods.append(nm)
        
    #Determine which modules are nested in which
    for m in mods:
        for n in mods:
            if m!=n:
                if m.a<n.a and m.b>n.b:
                    n.parent = m
                    m.children.append(n)
    
#     for m in mods:
#         print(m.parent,m.children)
    



class ModuleType(Enum):
    PART = 0
    RESOURCE = 1
    MODULE = 2
    PROPELLANT = 3


#===============================================================================
# Asset and its subclasses
#===============================================================================
class Asset():
    def __init__(self,**kwargs):
        if 'ix' in kwargs:
            ix = kwargs['ix']
            self.a = ix[0]
            self.b = ix[1]
            
        self.parent = None
        self.children = []
            
    

class Propellant(Asset):
    def __init__(self,**kwargs):
        Asset.__init__(self,**kwargs)

class Resource(Asset):
    def __init__(self,resourceLines,**kwargs):
        Asset.__init__(self,**kwargs)
        
        self.name = None
        self.amount = None
        self.maxAmount = None
        #print(resourceLines)
        self.readLines(resourceLines)

        
    def readLines(self,lines):
        
            
        thelines =  [line.split('=') for line in lines if '=' in line]
        md={}
        for line in thelines:
#             print(line)
            k = line[0].strip()
            v = line[1].strip()
            if v.isdigit():
                v = float(v)
            #print(k,v)
            md[k]=v
#         print(md) 
        if 'name' in md:
            self.name = md['name']
        if'amount' in md:
            self.amount = md['amount']
        if 'maxAmount' in md:
            self.maxAmount= md['maxAmount']
        
    def __repr__(self):
        return "name = %s\namount = %s\nmaxAmount = %s\n"%(self.name,self.amount, self.maxAmount)      


    
class Module(Asset):
    def __init__(self,modulelines,**kwargs):
        Asset.__init__(self,**kwargs)
        #print(modulelines)
        
        self.lines=modulelines
    
        

    
    def __repr__(self):
        return 'Module(%s,%s)'%(self.a,self.b)
    

    
    

    
        
class Part(Asset):
    def __init__(self,partFile,**kwargs):
        Asset.__init__(self,**kwargs)        

#     def readPartFile(self):
#         with open(self.partFile,'r') as f:
#             cntr = None
#             
#             #lines = [line.strip() for line in f.readlines()]
#             lines = f.readlines()
#             
#             ix = [i for i,x in enumerate(lines) if '{' in x]
#             lines=lines[ix[0]:]
#             
#             for i,line in enumerate(lines):
#                 if '{' in line:
#                     cntr = 1
                    
                        
        
        print('done reading file')
#             
#             
#             modi = [i for i,x in enumerate(lines) if '{' in x]
#             modj = [i for i,x in enumerate(lines) if '}' in x]
#             
# 
#             
#             modules =[]
#             
#             ii = modi[0]
#             jj = modj[-1]
#             modi = modi[1:]
#             modj = modj[:-1]
# #             print(modi,modj)
#             
#             for i,x in enumerate(modi):
#                 modules.append(lines[modi[i]-1:modj[i]+1])
#             
#             
#             for module in modules:
#                
#                 if module[0]=='RESOURCE':
#                     newresource = Resource(module)
#                     self.resources.append(newresource)
#                 elif module[0]=='MODULE':
#                     print('do module stuff')
#            
#             
#             
#             
#             
            
#             for i in range(len(modi)-1):
#                 #print(modi[i-1],modj[i])
#                 ii = modi[i-1]
#                 jj = modj[len(modi)-i-1]
#                 items.append(lines[ii:jj+1])
#                 print(ii,jj+1)
            
        
     


            

                
    
    def __repr__(self):
        return 'stuff'


if __name__=='__main__':
    parts = {}
    for d in os.listdir(pfn):
        fn = '//'.join((pfn,d,'part.cfg'))
        print(fn)
        readPartFile(fn)
        
        

    
    

