import numpy as np
from .config import glob, args, opts
import copy

class Engine:

	def __init__(self, args, game):

		self.args = copy.deepcopy(args)
		self.game = game
		self.player = game.player
		self.flock  = game.npcs
		self.blocks = game.blocks
		self.build_flock()

	def build_flock(self):
		self.x = np.zeros((self.args.n+1),dtype=float)
		self.y = np.zeros((self.args.n+1),dtype=float)

	def reach_target(self, target):
		for f in self.flock:
			if self.close3(f,target,target.r):
				if self.close3(self.player,target,2*self.args.r):
					f.arrived = True
					self.game.score += 1
		
	def update(self, dt):

		# Retrieve Player coordinates
		self.x[-1] = self.player.x
		self.y[-1] = self.player.y
		self.x[:-1] = np.array([f.x for f in self.flock])
		self.y[:-1] = np.array([f.y for f in self.flock])

		# Compute new angle 
		vx = [f.vx for f in self.flock] + [self.player.vx]
		vy = [f.vy for f in self.flock] + [self.player.vy]

		theta = self.move_step(vx, vy) % (2*np.pi)
		for i,f in enumerate(self.flock):
			f.tar_angle = float(theta[i,0])

		for b in self.blocks:
			for f in self.flock:
				self.colision(b,f)
			self.colision(b,self.player, r=1.0, angle=False)

		if opts.scen == 1: # PESCI
			if self.player.y < self.player.sprite.get_size()[1]/2 :
				self.player.vy *= -1
				self.player.y = self.player.sprite.get_size()[1]/2*1.1
			if self.player.y > glob.SH - self.player.sprite.get_size()[1]/2:
				self.player.vy *= -1
				self.player.y = glob.SH - self.player.sprite.get_size()[1] / 2 * 1.1
			for f in self.flock:
				if f.y < f.sprite.get_size()[1] / 2:
					f.vy *= -1
					f.y = f.sprite.get_size()[1] / 2 * 1.1
				if f.y > glob.SH - f.sprite.get_size()[1] / 2:
					f.vy *= -1
					f.y = glob.SH - f.sprite.get_size()[1] / 2 * 1.1

		if opts.mode == 1:
			target = self.game.target
			self.reach_target(target)

		self.player.update(dt)
		for i,f in enumerate(self.flock):
			f.update(dt)

	def close(self,ii,jj,r=None):
		if r is None: r=self.args.r
		dist = np.sqrt((self.x[ii] - self.x[jj])**2 + (self.y[ii] - self.y[jj])**2)
		return dist < r
	
	def close2(self,p1,p2,r):
		dist = np.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)
		return dist < (p1.r+p2.r)*r

	def close3(self,p1,p2,r):
		dist = np.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)
		return dist < r

	def colision(self, b, f, r=1.1, angle=True):
		if not self.close2(b, f, r): return
		new_angle = 2*np.atan2(b.y-f.y,b.x-f.x)-f.dir_angle/360*(2*np.pi)
		if angle: f.tar_angle = -new_angle
		vmod = np.sqrt((f.x-b.x)**2+(f.y-b.y)**2)
		f.x = b.x + (f.x-b.x)/vmod*max(b.r+f.r+10, 0*b.r*1.5)
		f.y = b.y + (f.y-b.y)/vmod*max(b.r+f.r+10, 0*b.r*1.5)

	def connect(self):
		A = np.zeros((self.args.n+1,self.args.n+1))
		for ii in range(self.args.n+1):
			A[ii,ii] = 1
			for jj in range(ii + 1, self.args.n+1):
				if self.close(ii,jj):
					A[ii, jj] = 1
					A[jj, ii] = 1
		A[-1,:] *= self.args.w
		A[:,-1] *= self.args.w
		A[-1,-1] = 1

		D = np.sum(A, axis=1).reshape(-1,1)
		F = (1/D)*A
		return F

	def move_step(self, vx, vy):

		F = self.connect()
		
		vx = np.dot(F, np.array(vx)[...,None])
		vy = np.dot(F, np.array(vy)[...,None])

		theta = np.atan2(vy,vx)
		noise = (np.random.rand(self.args.n+1, 1) - 0.5) * np.pi/2
		return theta + noise*self.args.noise
