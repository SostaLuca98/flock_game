import numpy as np

class Engine:

	def __init__(self, args, player, flock, blocks):

		self.args = args
		self.player = player
		self.flock  = flock
		self.blocks = blocks
		self.n = self.args.n # Flock Members (not leader)
		self.w = self.args.w # Leader Weight
		self.build_flock()

	@property
	def N(self):
		return self.n + 1

	def build_flock(self):
		self.x = np.zeros((self.N),dtype=float)
		self.y = np.zeros((self.N),dtype=float)
		
	def update(self, dt):

		# Retrieve Player coordinates
		self.x[-1] = self.player.x
		self.y[-1] = self.player.y
		self.x[:-1] = np.array([f.x for f in self.flock])
		self.y[:-1] = np.array([f.y for f in self.flock])

		# Compute new angle 
		vx = [f.vx for f in self.flock] + [self.player.vx]
		vy = [f.vy for f in self.flock] + [self.player.vy]

		#theta = [(f.dir_angle/(360)*2*np.pi)%2*np.pi for f in self.flock] + [self.player.tar_angle%(2*np.pi)]
		theta = self.move_step(vx, vy) % (2*np.pi)
		
		# AGGIUNGI COLLISIONI

		self.player.update(dt)
		for i,f in enumerate(self.flock):
			f.tar_angle = float(theta[i,0])
			f.update(dt)

	def close(self,ii,jj):
		dist = np.sqrt((self.x[ii] - self.x[jj])**2 + (self.y[ii] - self.y[jj])**2)
		return dist < self.args.r
	
	def connect(self):
		A = np.zeros((self.N,self.N))
		for ii in range(self.N):
			A[ii,ii] = 1
			for jj in range(ii + 1, self.N):
				if self.close(ii,jj):
					A[ii, jj] = 1
					A[jj, ii] = 1
		A[-1,:] *= self.w
		A[:,-1] *= self.w
		A[-1,-1] = 1

		D = np.sum(A, axis=1).reshape(-1,1)
		F = (1/D)*A
		return F

	def move_step(self, vx, vy):

		F = self.connect()
		
		vx = np.dot(F, np.array(vx)[...,None])
		vy = np.dot(F, np.array(vy)[...,None])
		theta = np.atan2(vy,vx)

		noise = (np.random.rand(self.N, 1) - 0.5) * np.pi/2
		return theta + noise

#D = np.diag(np.sum(A, axis=1))
#F = np.linalg.solve(D, A)