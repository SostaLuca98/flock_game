import numpy as np
from .config import glob, args, opts
import copy
import pygame

class Collider:

	def __init__(self, args, game) -> None:

		self.args = args
		self.game = game
		self.target = self.game.target

	@staticmethod
	def obstacle_entity(b, f, r=1.1, angle=True):

		def dist_obstacle(p1,p2,r):
			dist = np.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)
			return dist < (p1.r+p2.r)*r

		if not dist_obstacle(b, f, r): return
		new_angle = 2*np.arctan2(b.y-f.y,b.x-f.x)-f.dir_angle/360*(2*np.pi)
		if angle: f.tar_angle = -new_angle
		vmod = np.sqrt((f.x-b.x)**2+(f.y-b.y)**2)
		f.x = b.x + (f.x-b.x)/vmod*max(b.r+f.r+10, 0*b.r*1.5)
		f.y = b.y + (f.y-b.y)/vmod*max(b.r+f.r+10, 0*b.r*1.5)

		return
	
	@staticmethod
	def boundary_y_player(player):

		if player.y < player.sprite.get_size()[1]/2 :
			player.vy *= -1
			player.y = player.sprite.get_size()[1]/2*1.1
		if player.y > glob.SH - player.sprite.get_size()[1]/2:
			player.vy *= -1
			player.y = glob.SH - player.sprite.get_size()[1] / 2 * 1.1

		return player
	
	@staticmethod
	def boundary_y_npc(npc):

		if npc.y < npc.sprite.get_size()[1] / 2:
			npc.vy *= -1
			npc.y = npc.sprite.get_size()[1] / 2 * 1.1
		if npc.y > glob.SH - npc.sprite.get_size()[1] / 2:
			npc.vy *= -1
			npc.y = glob.SH - npc.sprite.get_size()[1] / 2 * 1.1
		
		return npc

	def reach_target(self, player, npc):

		def dist_target(p1,p2,r):
			dist = np.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)
			return dist < r
		
		if dist_target(npc,self.target,self.target.r):
			if dist_target(player,self.target,2*self.args.r):
				npc.arrived = True
				self.game.score += 1
		
		return

class Engine:

	def __init__(self, args, game):

		self.args = copy.deepcopy(args)
		self._build_flock()

		self.game = game
		self.collider = Collider(args, game)
		
		self.player = game.player
		self.flock  = game.npcs
		self.blocks = game.blocks

		self.pacman_x = True
		self.pacman_y = (opts.scen != 1) # PESCI
		self.render_graph = (opts.mode == 2)
		self.connectivity_mode = ["smoothing", "binary"][0]

	def _build_flock(self):

		dim = self.args.n+1
		self.x  = np.zeros((dim), dtype=float)
		self.y  = np.zeros((dim), dtype=float)
		self.A  = np.zeros((dim,dim), dtype=float)
		self.Dx = np.zeros((dim,dim), dtype=float)
		self.Dy = np.zeros((dim,dim), dtype=float)

		return
	
	def _compute_delta(self):

		def toroidal_delta(i, j):

			dx, dy = (self.x[j] - self.x[i], self.y[j] - self.y[i])
			if self.pacman_x: dx = (dx + glob.SW/2) % glob.SW - glob.SW/2
			if self.pacman_y: dy = (dy + glob.SH/2) % glob.SH - glob.SH/2
			
			return dx, dy

		dim_flock = self.args.n
		for ii in range(dim_flock+1):
			self.Dx[ii, ii], self.Dy[ii, ii] = 0, 0
			for jj in range(dim_flock+1):
				dx, dy = toroidal_delta(ii, jj)
				self.Dx[ii, jj], self.Dy[ii, jj] = dx, dy

		return

	def _move_step(self, vx, vy):

		def build_influence_matrix():

			def smoothing_function(d, r, c1=0.25, c2=1.5, exp=2.0):
				return np.exp(-(1/c1) * (d / (c2*r)) ** exp)

			def binary_function(d, r):
				return (d < r).astype(float)

			# Precompute distance matrix once
			self.R = np.sqrt(self.Dx**2 + self.Dy**2)

			# Select influence rule
			if self.connectivity_mode == "smoothing":
				self.A = smoothing_function(self.R, self.args.r)
			elif self.connectivity_mode == "binary":
				self.A = binary_function(self.R, self.args.r)
			else:
				raise ValueError(f"Unknown mode: {self.connectivity_mode}")

		def connect():			

			build_influence_matrix()

			self.A[-1,:] *= self.args.w
			self.A[:,-1] *= self.args.w
			self.A[-1,-1] = 1

			D = np.sum(self.A, axis=1).reshape(-1,1)
			F = (1/D)*self.A

			return F

		F = connect()
		
		vx = np.dot(F, np.array(vx)[...,None])
		vy = np.dot(F, np.array(vy)[...,None])

		theta = np.arctan2(vy,vx)
		noise = (np.random.rand(self.args.n+1, 1) - 0.5) * np.pi/2

		return theta + noise*self.args.noise
	
	def _check_collisions(self):

		for b in self.blocks:
			for f in self.flock:
				self.collider.obstacle_entity(b,f)
			self.collider.obstacle_entity(b, self.player, r=1.0, angle=False)

		if opts.scen == 1: # PESCI
			for f in self.flock:
				self.collider.boundary_y_npc(f)
			self.collider.boundary_y_player(self.player)

		if opts.mode == 1: # COMPETITIVA
			for f in self.flock:
				self.collider.reach_target(self.player, f)

		return
		
	def update(self, dt):

		# Retrieve Player coordinates
		self.x = np.array([f.x for f in self.flock]+[self.player.x])
		self.y = np.array([f.y for f in self.flock]+[self.player.y])

		# Compute new angle 
		vx = [f.vx for f in self.flock] + [self.player.vx]
		vy = [f.vy for f in self.flock] + [self.player.vy]

		self._compute_delta()
		theta = self._move_step(vx, vy) % (2*np.pi)
		for i,f in enumerate(self.flock):
			f.tar_angle = float(theta[i,0])

		self._check_collisions()
		self.player.update(dt)
		for i,f in enumerate(self.flock): f.update(dt)

	def render(self, screen: pygame.Surface) -> None:

		if not self.render_graph: return

		max_influence = self.args.w
		
		def influence_to_color(value, is_last_node=False):
			if is_last_node:
				# Color gradient from strong orange to faint orange
				strong_color = np.array([254, 117, 20], dtype=float)
				faint_color  = np.array([255, 200, 140], dtype=float)  # pale orange
				# Normalize value to [0,1]
				t = np.clip(value / max_influence, 0, 1)
			
			else:
				# Grayscale with a lower bound = light grey
				strong_color = np.array([0, 0, 0], dtype=float)  # dark grey
				faint_color = np.array([240, 240, 240], dtype=float)  # light grey
				# Normalize value to [0,1]
				t = np.clip(value, 0, 1)

			# Interpolate color
			color = t * strong_color + (1 - t) * faint_color
			return tuple(color.astype(int))

		def draw_line(p1,p2,color=(127,127,127),width=1):
			pygame.draw.line(screen, color, (p1[0]*glob.SF,p1[1]*glob.SF), (p2[0]*glob.SF,p2[1]*glob.SF), width)

		dim_flock = self.A.shape[0]-1
		for i in range(dim_flock+1):
			for j in range(i):
				if self.A[i, j] < 1e-4 * self.args.n: continue
	
				color = influence_to_color(self.A[i, j], is_last_node=(i == dim_flock))
				draw_line((self.x[i], self.y[i]), (self.x[i]+self.Dx[i,j], self.y[i]+self.Dy[i,j]), color=color)
				draw_line((self.x[j], self.y[j]), (self.x[j]+self.Dx[j,i], self.y[j]+self.Dy[j,i]), color=color)