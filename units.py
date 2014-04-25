


def convertTime(time,inputunits,outputunits):
	i = _toseconds(inputunits)
	f = _toseconds(outputunits)
	print(i,f)
	return float(time)*i/f

def convertDistance(distance,inputunits,outputunits):
	i = _tometers(inputunits)
	f = _tometers(outputunits)

	return float(distance)*i/f

def _toseconds(units):
	to_seconds = 0
	print(units)
	if units == 's':
		to_seconds = 1
		print('seconds')
	elif units =='m':
		to_seconds = 60
		print('minutes')
	elif units=='h':
		to_seconds = 60*60
		print('hours')
	elif units =='d':
		to_seconds = 60*60*24
		print('days')
	elif units=='a':
		to_seconds = 60*60*24*365.25
		print('years')
	else:print('not found')
		#assert False,'units._toseconds unit not recognized'

	return to_seconds

def _tometers(units):
	to_meters = 0
	print(units)
	if units == 'm':
		to_meters = 1
		print('meters')
	elif units =='km':
		to_meters = 1e3
		print('kilometers')
	elif units=='Mm':
		to_meters = 1e6
		print('megameters')
	elif units =='Gm':
		to_meters= 1e9
		print('gigameters')
	else:print('not found')
	return to_meters