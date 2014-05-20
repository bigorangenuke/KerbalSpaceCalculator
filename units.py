

dbg = False

def ctime(time,inputunits,outputunits):
	return convertTime(time,inputunits,outputunits)

def cdist(distance,inputunits,outputunits):
	return convertDistance(distance,inputunits,outputunits)

def convertTime(time,inputunits,outputunits):
	i = _toseconds(inputunits)
	f = _toseconds(outputunits)
	if dbg:print(i,f)
	return float(time)*i/f

def convertDistance(distance,inputunits,outputunits):
	i = _tometers(inputunits)
	f = _tometers(outputunits)

	return float(distance)*i/f

def _toseconds(units):
	to_seconds = 0
	if dbg:print(units)
	if units == 's':
		to_seconds = 1
		if dbg:print('seconds')
	elif units =='m':
		to_seconds = 60
		if dbg:print('minutes')
	elif units=='h':
		to_seconds = 60*60
		if dbg:print('hours')
	elif units =='d':
		to_seconds = 60*60*24
		if dbg:print('days')
	elif units=='a':
		to_seconds = 60*60*24*365.25
		if dbg:print('years')
	else:print('not found')
		#assert False,'units._toseconds unit not recognized'

	return to_seconds

def _tometers(units):
	to_meters = 0
	if dbg:print(units)
	if units == 'm':
		to_meters = 1
		if dbg:print('meters')
	elif units =='km':
		to_meters = 1e3
		if dbg:print('kilometers')
	elif units=='Mm':
		to_meters = 1e6
		if dbg:print('megameters')
	elif units =='Gm':
		to_meters= 1e9
		if dbg:print('gigameters')
	else:print('not found')
	return to_meters