#Parsing parts files
import os
pfn = 'F://Games//KMP//Squad//Parts//Engine'
import itertools
from collections import Counter
from pyparsing import nestedExpr

import re



class Resource():
    def __init__(self,resourceLines):
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

class Module():
    def __init__(self,modulelines):
        self.lines=modulelines
        
def readPartFile(partFile):
    
    f = open(partFile,'r')
    lines = f.readlines()
    f.close()

    startlines = st = [i for i,line in enumerate(lines) if '{' in line]
    endlines = en = [i for i,line in enumerate(lines) if '}' in line]

    assert len(startlines)==len(endlines),'File incomplete'

    #Add the lists together
    dl = st+en
    
    #O
    modlst = []

    x = 0
    
    #When the index comes from start positions, a new list object is added to modlst with a zero in place of the last item
    #When the index comes from an end position, it walks backwards up the modlst until it find a list that has a zero in the last item
    #This value is accepted and the 
    for d in dl:
        print(d)
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
                    break
                
    print(modlst)
    

    


    
         
        
        
    
        
class Part():
    def __init__(self,partFile):
        
        self.partFile = partFile
        self.resources = []
        readPartFile(partFile)
        
        

    def readPartFile(self):
        with open(self.partFile,'r') as f:
            cntr = None
            
            #lines = [line.strip() for line in f.readlines()]
            lines = f.readlines()
            
            ix = [i for i,x in enumerate(lines) if '{' in x]
            lines=lines[ix[0]:]
            
            for i,line in enumerate(lines):
                if '{' in line:
                    cntr = 1
                    
                        
                        
                    
            
            
       
          
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
            
          
    
                    
            
        
            
            
            
            
            
#             while F:
#                 line = f.readline()
#       
#                 if 'PART' in line:
#                     print('do part stuff')
#                     
#                 if 'RESOURCE' in line:
#                     print('do resource stuff')
                
            
            
                    
            #thelines = [line.strip().split('=') for line in f.readlines()  if '=' in line]
            
            
            
#             dict = {}
#             for line in thelines:
#                 dict[line[0]]=line[1]
#             
#             self.partDict = dict
            

                
    
    def __repr__(self):
        return 'stuff'


if __name__=='__main__':
    parts = {}
    for d in os.listdir(pfn):
        fn = '//'.join((pfn,d,'part.cfg'))
        prt = Part(fn)
        parts[d]=prt
        print(prt.resources)
        break
        
        
        
#     
#     for k,part in parts.items():
#         print(part.partDict)
#         for k,v in part.partDict.items():
#             print(k,v)
#         break
#     
    
    

