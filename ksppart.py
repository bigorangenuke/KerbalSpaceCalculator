#Parsing parts files
import os
import glob
pfn = 'F://Games//KMP//Squad//Parts//'


from enum import Enum
types = ['PART','RESOURCE','MODULE','PROPELLANT']

class ModuleType(Enum):
    PART = 0
    RESOURCE = 1
    MODULE = 2
    PROPELLANT = 3
    GENERIC = 4
    ENGINE = 5
    SCIENCE = 6

#find the curly braces in the part.cfg file
def findModules(lines):
    startlines  = [i for i,line in enumerate(lines) if '{' in line]
    endlines  = [i for i,line in enumerate(lines) if '}' in line]
    
    assert len(startlines)==len(endlines),'File incomplete\n%s'%(lines)
    return startlines,endlines

#removes None values from a list without changing the order of the values
def removeNone(lines):
    return [line for line in lines if line is not None]


#removes lines that are considered comments
#This does not allow comments at the end of a line
def removeComments(lines,delim = '//'):
    for i,line in enumerate(lines):
        if delim in line[:5]:
            lines[i] = None
    return removeNone(lines)

#remove the header words such as PART and PROPELLANT
#deletes the whole line that contains the type word
def removeHeaders(lines):
    
    for i in range(len(lines)):
        if any(thetype in lines[i] for thetype in types):
            lines[i] = None
    
    return lines

#remove lines that contain curly braces
def removeBraces(lines):
    lines = removeNone(lines)
    for i, line in enumerate(lines):
        if '{' in line or '}' in line:
            lines[i]=None
    return lines

                 
def removeSubModules(lines):

    x = 0
    for i,line in enumerate(lines):
        
        if '{' in line:
            x +=1

        if x>1:
            lines[i]=None
            
        if '}' in line:
            x -=1

        if any(thetype in line for thetype in types):
            lines[i] = None
    
           
    lines = removeBraces(lines)
    return removeNone(lines)

#splits the list
def linesToDict(lines):
    d = {}
    
    for i,l in enumerate(lines):
        
        k = l[0].strip()
        v = l[1].strip()
        if v.isdigit():
            v = float(v)
        
        d[k]=v
        
    return d

#===============================================================================
# Reads the part.cfg file
#===============================================================================
def readPartFile(partFile):
    f = open(partFile, 'r')
    lines = f.readlines()
    f.close()
    lines= removeComments(lines)
    
    lines = [line.strip() for line in lines if line != '\n']

    for i,line in enumerate(lines):
        if '=' in line:
            lines[i] = line.split('=')
    
    lines = [line for line in lines if line]

    st,en = findModules(lines)
    
    assert len(st)==len(en),'File incomplete'
    
    #Add the lists together
    dl = st+en
    
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
        
        
        mln = None
        
        
        
    
        if any(thetype in lines[a] for thetype in types):
            mln = lines[a:b+1]
        else:
            mln = lines[a-1:b+1]
            
        
        #print('LINES:\t',lines[a-1],lines[a],lines[b],lines[b])
        #print(a -1,b+1)
        #print(mln)
        
        mt = mln[0].strip()
        
        #print('MODULE TYPE =',mt)
        moduleType=None
        
        
        
        
        #print(a,b)
        nm = None
        if 'PART' in mt:
            moduleType = ModuleType.PART
            nm = Part(mln,ix = m)
        elif 'RESOURCE' in mt:
            moduleType = ModuleType.RESOURCE
            nm = Resource(mln,ix = m)
        elif 'PROPELLANT' in mt:
            nm = Propellant(mln,ix = m)
            moduleType = ModuleType.PROPELLANT
        elif 'MODULE' in mt:
            moduleType = ModuleType.MODULE
            nm = Module(mln,ix=m)

        else:
            moduleType = ModuleType.GENERIC
            nm = GenericModule(mln,ix=m)
            #assert False,'Module type %s not recognized'%(mt)
        
        
        

        mods.append(nm)
        
    #Determine which modules are nested in which
    for m in mods:
        for n in mods:
            if m!=n:
                if m.a<n.a and m.b>n.b:
                    n.parent = m
                    m.children.append(n)
    
    #Check that no module has the same module as parent and child
    for m in mods:
        if m.parent and m.children:
            if m.parent in m.children:
                assert False,'Bad trouble.  Parent-Child hierarchy is broken.  Corrupt file or error in the parser'
    return mods
#     for m in mods:
#         print(m.parent,m.children)
    






#===============================================================================
# Asset and its subclasses
#===============================================================================
class Asset():
    def __init__(self,**kwargs):
        if 'ix' in kwargs:
            ix = kwargs['ix']
            self.a = ix[0]
            self.b = ix[1]
        self.name = None
        self.moduleType = None
        self.dict = {}
        
        self.parent = None
        self.children = []
    
    def __repr__(self):
        return '%s %s'%(self.moduleType,self.name)
    
        
    
class GenericModule(Asset):
    def __init__(self,lines,**kwargs):
        Asset.__init__(self,**kwargs)
        self.moduleType = ModuleType.GENERIC
        self.dict=linesToDict(removeSubModules(lines))
        self.mapDictToAttr(self.dict)
    def mapDictToAttr(self,d):
        if 'name' in d:
            self.name = d['name']
        
            
        
class Propellant(Asset):
    def __init__(self,lines,**kwargs):
        Asset.__init__(self,**kwargs)
        self.moduleType = ModuleType.PROPELLANT
        self.set_dict(linesToDict(removeSubModules(lines)))
        
        self.ratio = None
    
    def set_dict(self,d):
        
        self.mapDictToAttr(d)
        self.dict = d
        
    def mapDictToAttr(self,d):
        if 'name' in d:
            self.name = d['name']
        if'ratio' in d:
            self.amount = d['ratio']
    
    

class Resource(Asset):
    def __init__(self,lines,**kwargs):
        Asset.__init__(self,**kwargs)
        self.moduleType = ModuleType.RESOURCE
        self.amount = None
        self.maxAmount = None
        
        self.set_dict(linesToDict(removeSubModules(lines)))
        
    def set_dict(self,d):
        
        self.mapDictToAttr(d)
        self.dict = d
        
        
    def mapDictToAttr(self,d):
        if 'name' in d:
            self.name = d['name']
        if'amount' in d:
            self.amount = d['amount']
        if 'maxAmount' in d:
            self.maxAmount= d['maxAmount']   


    
class Module(Asset):
    def __init__(self,lines,**kwargs):
        Asset.__init__(self,**kwargs)
        self.moduleType = ModuleType.MODULE
        self.set_dict(linesToDict(removeSubModules(lines)))
        
    def set_dict(self,d):
        self.mapDictToAttr(d)
        self.dict = d
    
    def mapDictToAttr(self,d):
        if 'name' in d:
            self.name = d['name']
        if'amount' in d:
            self.amount = d['amount']
        if 'maxAmount' in d:
            self.maxAmount= d['maxAmount']   
    
        
class Part(Asset):
    def __init__(self,partLines,**kwargs):
        Asset.__init__(self,**kwargs)   
        self.moduleType = ModuleType.PART     
        self.pdict = self.readLines(partLines)
        self.mapDictToAttr(self.pdict)
        

    def readLines(self,lines):
        #returns a list of all of the values from the cfg file
        nlines = removeSubModules(lines)
        d = linesToDict(nlines)
        return d
        
    def mapDictToAttr(self,d):
        if 'name' in d:
            self.name = d['name']

    

if __name__=='__main__':
    parts = []
    
#     
#     fn = os.path.join(pfn,'Command','probeCoreHex','part.cfg')
#     print(fn)
#     readPartFile(fn)
#  
#      
    for root,dirs,files in os.walk(pfn):
        if 'part.cfg' in files:
 
            fn = os.path.join(root,'part.cfg')
            parts.append(readPartFile(fn))
             


        

    
    print('done reading files')
        #break
        
        

    
    

