import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

"""
Create Your Own Lattice Boltzmann Simulation (With Python)
Philip Mocz (2020) Princeton Univeristy, @PMocz
# 
Simulate flow past different geometric objects
for an isothermal fluid

"""


class LBM:
	def __init__(self, Nx=400, Ny=100, Nt=4000, plotEveryNth=10, rho0=100, tau=0.6, flowDirection=3, objects=[], plotType='Speed', plotRealTime=True, fileName='LBM.png') -> None:
		#plotType is one of ['Vorticity','Divergence','Speed','Density','Momentum']
		#Simulation parameters given in constructor
		self.Nx = Nx
		self.Ny = Ny
		self.Nt = Nt
		self.rho0 = rho0
		self.tau = tau
		self.plotType = plotType
		self.plotRealTime = plotRealTime
		#Lattice speeds/weights
		self.NL = 9
		self.idxs = np.arange(self.NL)
		self.cxs = np.array([0, 0, 1, 1, 1, 0,-1,-1,-1])
		self.cys = np.array([0, 1, 1, 0,-1,-1,-1, 0, 1])
		self.weights = np.array([4/9,1/9,1/36,1/9,1/36,1/9,1/36,1/9,1/36]) # sums to 1
		self.flowDirection = flowDirection
		self.fileName = fileName
		self.plotEveryNth = plotEveryNth

		#Initial conditions
		self.F = self.initialize()
		self.objects = objects


		#Start the simulation
	def run(self):
		for it in range(self.Nt):
			#print(it)
			
			# Drift
			self.drift()
			
			# Set reflective boundaries
			for obj in self.objects:
				bndry = self.F[obj.getObject(),:]
				bndry = bndry[:,[0,5,6,7,8,1,2,3,4]]
				obj.setBoundary(bndry)
			
			# Calculate fluid variables
			self.rho = np.sum(self.F,2)
			self.ux  = np.sum(self.F*self.cxs,2) / self.rho
			self.uy  = np.sum(self.F*self.cys,2) / self.rho

			# Apply Collision
			self.collision()


			# Apply boundary
			for obj in self.objects:
				self.F[obj.getObject(),:] = obj.getBoundary()
			
			
		# plot in real time - color 1/2 particles blue, other half red
			if (self.plotRealTime and (it % self.plotEveryNth) == 0) or (it == self.Nt-1):
				plt.cla()
				for obj in self.objects:
					self.ux[obj.getObject()] = 0
					self.uy[obj.getObject()] = 0

				#vorticity
				if self.plotType == 'Vorticity':
					vorticity = (np.roll(self.ux, -1, axis=0) - np.roll(self.ux, 1, axis=0)) - (np.roll(self.uy, -1, axis=1) - np.roll(self.uy, 1, axis=1))
					self.plotting(vorticity, it, cmap='bwr')

				elif self.plotType == 'Divergence':
					divergence = (np.roll(self.ux, -1, axis=0) - np.roll(self.ux, 1, axis=0)) + (np.roll(self.uy, -1, axis=1) - np.roll(self.uy, 1, axis=1))
					#divergence = (np.roll(self.ux, -1, axis=1) - np.roll(self.ux, 1, axis=1)) + (np.roll(self.uy, -1, axis=0) - np.roll(self.uy, 1, axis=0))
					#dont know what it is
					self.plotting(divergence, it, cmap='bwr')
				
				#speed
				elif self.plotType == 'Speed':
					speed = np.sqrt(self.ux**2+self.uy**2)
					self.plotting(speed, it=it)

				#density
				elif self.plotType == 'Density':
					density = self.rho
					self.plotting(density, it=it)

				elif self.plotType == 'Momentum':
					momentum = self.rho*(self.ux+self.uy)
					self.plotting(momentum, it=it)
				
				plt.clim(-.1, .1)
				ax = plt.gca()
				#ax.invert_yaxis()
				ax.get_xaxis().set_visible(False)
				ax.get_yaxis().set_visible(False)	
				ax.set_aspect('equal')
				plt.pause(1.0)


		# Save figure
		plt.savefig(self.fileName,dpi=240)
		plt.show()
	
	def initialize(self):
		F = np.ones((self.Ny,self.Nx,self.NL)) #* rho0 / NL
		np.random.seed(42)
		F += 0.01*np.random.randn(self.Ny,self.Nx,self.NL)
		X, Y = np.meshgrid(range(self.Nx), range(self.Ny))
		F[:,:,self.flowDirection] += 2 * (1+0.2*np.cos(2*np.pi*X/self.Nx*4))
		rho = np.sum(F,2)
		for i in self.idxs:
			F[:,:,i] *= self.rho0 / rho
		
		return F
	
	def drift(self):
		for i, cx, cy in zip(self.idxs, self.cxs, self.cys):
				self.F[:,:,i] = np.roll(self.F[:,:,i], cx, axis=1)
				self.F[:,:,i] = np.roll(self.F[:,:,i], cy, axis=0)
	

	def collision(self):
		Feq = np.zeros(self.F.shape)
		for i, cx, cy, w in zip(self.idxs, self.cxs, self.cys, self.weights):

			Feq[:,:,i] = self.rho * w * ( 1 + 3*(cx*self.ux+cy*self.uy)  + 9*(cx*self.ux+cy*self.uy)**2/2 - 3*(self.ux**2+self.uy**2)/2 )
		
		self.F += -(1.0/self.tau) * (self.F - Feq)
	
	def plotting(self, arr, it, cmap='viridis'):
		for obj in self.objects:
			arr[obj.getObject()] = np.nan
			arr = np.ma.array(arr, mask=obj.getObject())

		#print('plot arr')
		plt.imshow(arr, cmap=cmap, alpha=1.0)

		for obj in self.objects:
			#print('plot obj')
			plt.imshow(~obj.getObject(), cmap='gray', alpha=0.3)
			