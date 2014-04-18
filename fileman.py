import csv

def extractDataColumns(filename,**kwargs):
	numColumns = 2
	delimiters = [',']
	print('start')
	
	with open(filename,'r') as f:
		print('open file')
		if 'columns' in kwargs:
			numColumns = kwargs['columns']
		if 'delimiter' in kwargs:
			delimiters = list(kwargs['delimiter'])

		l = []
		#Check for comments
		print('enter loop')
		for line in (x for x in f if not x.startswith('#')):
			#Iterate over the delimiters
			for d in delimiters:
				if len(line.split(d))>1:
					l.append([float(l.strip()) for l in line.split(d)])
					
		print('exit loop')

		f = list(zip(*l))

		if len(f)==2:
			return list(f[0]),list(f[1])
		else:
			return list(f[0]),list(f[1:])

def saveFile(filename):
	print('fileman.saveFile')	


def appendFile(filename,lines):
	print('fileman.appendFile')
	line = [str(x) for x in lines]
	f=open(filename,'a')
	s = ','.join(line)
	s +='\n'
	f.write(s)
	f.close()
	
def loadFile(filename):
	print('fileman.loadFile')
	


	
	
	