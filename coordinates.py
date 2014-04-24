import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import copy 
cartesian = 0
spherical = 1
cylindrical =2

dbg = True

class Vector():
	def __init__(self,vector,coord_type=cartesian):
		assert coord_type<3,'coord_type must be one of 3 types. cartesian = %s, spherical = %s, cylindrical = %s'%(cartesian,spherical,cylindrical)
		self.vec = np.asarray(vector)
		self.type= coord_type
		self.unitVector = self.get_unitVector()
		self.magntiude = self.get_magnitude()

	def get_unitVector(self):
		if self.type==cartesian:
			print('stuff')
			return self.vec/self.get_magnitude()

	def get_magnitude(self):
		if self.type==cartesian:
			return np.linalg.norm(self.vec)
		elif self.type==spherical:
			return float(self.vec[0])
		elif self.type == cylindrical:
			return float(self.vec[0])
		else:
			assert False, 'coordinate type not recognized'
			

def cartesianToSpherical(*args,**kwargs):#x,y,z = 0):
	if dbg:print('coordinates.cartesianToSpherical')
	u = np.asarray(args)
	
	x = u[:,0]
	y = u[:,1]
	z = u[:,2]
	
	if kwargs:
		print('coordinates.cartesianToSpherical kwargs passed')
	
	r = np.sqrt(x*x+y*y+z*z)
	theta = np.arccos(z/r)
	phi = np.arctan(y/x)
	
	return np.column_stack((r,theta,phi))


def sphericalToCartesian(*args,**kwargs):#r,phi,theta=None):
	if dbg:print('coordinates.sphericalToCartesian')
	u = np.asarray(args)
	r = u[:,0]
	phi = u[:,1]
	theta = u[:,2]
	if kwargs:
		print('coordinates.sphericalToCartesian kwargs passed')
	


	x = r*np.sin(theta)*np.cos(phi)
	y = r*np.sin(theta)*np.sin(phi)
	z = r*np.cos(theta)
	
	return np.column_stack((x,y,z))

def cylindricalToCartesian(*args,**kwargs):
	u = np.asarray(args)
	
	rho = u[:,0]
	phi = u[:,1]
	z = u[:,2]
	if kwargs:
		print('coordinates.cylindricalToCartesian kwargs passed')
	
	x = rho*np.cos(phi)
	y = rho*np.sin(phi)
	
	return np.column_stack((x,y,z))
	
def cylindricalToSpherical(*args,**kwargs):
	
	u = np.asarray(args)
	
	rho = u[:,0]
	phi = u[:,1]
	z = u[:,2]
	if kwargs:
		print('coordinates.cylindricalToSpherical kwargs passed')


	r = np.sqrt(rho*rho+z*z)
	theta = np.arcsin(z/r)
	
	return np.column_stack((r,phi,theta))


def sphericalToCylindrical(*args,**kwargs):
	
	u = np.asarray(args)
	
	r = u[:,0]
	phi = u[:,1]
	theta = u[:,2]
	if kwargs:
		print('coordinates.sphericalToCylindrical kwargs passed')
		
	rho = r *np.cos(theta)
	z = r*np.sin(theta)
	return np.column_stack((rho,phi,z))

def unitSphericalToCartesian(theta,phi,r_hat,phi_hat,theta_hat=None):
	if dbg:print('coordinates.unitSphericalToCartesian')
	x_hat = np.sin(theta)*np.cos(phi)*r_hat + np.cos(theta)*np.cos(phi)*theta_hat - np.sin(phi)*phi_hat
	y_hat = np.sin(theta)*np.sin(phi)*r_hat + np.cos(theta) * np.sin(phi)*theta_hat + np.cos(phi) * phi_hat
	z_hat = np.cos(theta)*r_hat - np.sin(theta)*theta_hat


def unitCartesianToSpherical(theta,phi,x_hat,y_hat,z_hat = 0):
	if dbg:print('coordinates.unitCartesianToSpherical')
	r_hat = np.sin(theta)*np.cos(phi)*x_hat + np.sin(theta)*np.sin(phi)*y_hat  + np.cos(theta)*z_hat
	theta_hat = np.cos(theta)*np.cos(phi)*x_hat  + np.cos(theta)*np.sin(phi)*y_hat - np.sin(theta)*z_hat
	phi_hat = -np.sin(phi)*x_hat  + np.cos(phi)*y_hat
	return r_hat,theta_hat,phi_hat


def x_rotation(theta):
	if dbg:print('coordinates.x_rotation')
	xr = np.zeros((3,3))
	xr[0,0] = 1
	xr[1,1] = np.cos(theta)
	xr[2,1] = -np.sin(theta)
	xr[1,2] = np.sin(theta)
	xr[2,2] = np.cos(theta)
	return xr

def y_rotation(theta):
	if dbg:print('coordinates.y_rotation')
	yr = np.zeros((3,3))
	yr[0,0] = np.cos(theta)
	yr[2,0] = np.sin(theta)
	yr[1,1] = 1
	yr[0,2] = -np.sin(theta)
	yr[2,2] = np.cos(theta)
	return yr

def z_rotation(theta):
	if dbg:print('coordinates.z_rotation')
	zr = np.zeros((3,3))
	zr[0,0] = np.cos(theta)
	zr[1,1] = np.cos(theta)
	zr[2,2] = 1
	zr[0,1] = np.sin(theta)
	zr[1,0] = -np.sin(theta)
	return zr

def rotation(**kwargs):
	if dbg:print('coordinates.rotation')
	X = x_rotation(0)
	Y = y_rotation(0)
	Z = z_rotation(0)
	R = x_rotation(0)
	if 'x' in kwargs:
		R *= x_rotation(kwargs['x'])
	if 'y' in kwargs:
		R *= y_rotation(kwargs['y'])
		Y = y_rotation(kwargs['y'])
	if 'z' in kwargs:
		R *= z_rotation(kwargs['z'])
	return R


def plotVectors(vectors,coord_type=0):
	X,Y,Z=zip(*vectors)
	if coord_type==1:
		v = sphericalToCartesian(vectors)
		X,Y,Z=zip(*v)
	elif coord_type==2:
		v= cylindricalToCartesian(vectors)
		X,Y,Z=zip(*v)
		

	fig = plt.figure()
	ax = fig.add_subplot(111,projection='3d')
	#ax.quiver(X,Y,Z,angles='xy',scale_units='xy',scale = 1)
	
	for i in range(len(X)):
		ax.plot([0,X[i]],[0,Y[i]],[0,Z[i]])
	
	ax.set_xlim([-5,5])
	ax.set_ylim([-5,5])
	ax.set_zlim([-5,5])

	#plt.show()

	


if __name__=='__main__':

	#fig = plt.figure()
	#ax = fig.add_subplot(111,projection='3d')

	# v = [[1,1,1],[1,0,0],[1,np.pi*0.5,np.pi*0.5]]
	v = [0,0,1]
	u = np.array([1,1,1])

	#xrot = x_rotation(1.57)
	uu = np.dot(x_rotation(1.57),u)
	vv = np.dot(rotation(x=np.pi*0.25,y =np.pi*0.5,z = 0),u)
	print(vv)

	plotVectors([uu,v,vv])

	plt.show()