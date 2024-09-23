import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass

np.random.seed(1234)

Dati = {
	'n': 100, # Numero di elementi dello stormo
	'n_leaders': 10, # Numero di leader
	'tempo_max': 20, # Numero di istanti temporali simulati
	'plot_stride': 10, # plot ogni tot istanti (utile in sviluppo)
	'x_max': 1280, # Lunghezza del dominio
	'y_max': 720, # Altezza del dominio
	'init_x_max': 300,
	'init_y_max': 150,
	'init_theta_avg': 0,
	'init_theta_semispan': np.pi/6,
	'velocita': 1, # Lunghezza di 1 passo temporale
	'Ostacolo': 'Cerchio', # Forma dell'ostacolo da posizionare (Cerchio/No)
	'x_o': [80*x for x in [2, 8, 5, 3, 15, 15, 17.97, 9.3293, 6.7429, 13.7446, 3.9999, 7.5]],	 # Coordinata x centro ostacolo
	'y_o': [80*y for y in [3, 1, 0, 10, -0.4, 10.4, 8.8592, 1.8270, 8.3421, 5.8782, 6.3879, 5]], # Coordinata y centro ostacolo
	'r_o': [80*l for l in [1.0, 0.3, 0.2, 0.2, 0.8, 0.7, 0.4524, 0.7069, 0.7070, 0.9748, 0.869, 0.6]], # Larghezza dell'ostacolo
	'legame_lr': 0.0, #0.1, # Probabilità del legame lungo raggio
	'r': 10, # Raggio legame di vicinanza
}

# def fix_BC(Dati, x, y):
# 	for ii in range(Dati["n"]):
# 		# BCs periodiche in x
# 		if x[ii] < 0: x[ii] = x[ii] + Dati["x_max"]
# 		if x[ii] > Dati["x_max"]: x[ii] = x[ii] - Dati["x_max"]
# 		# BCs di riflesso in y
# 		if y[ii] < 0: y[ii] = 0
# 		if y[ii] > Dati["y_max"]: y[ii] = Dati["y_max"]
# 	return (x, y)

# def fix_BC_vel(Dati, x, y, u, v):
# 	tol = 0.02
# 	for ii in range(Dati["n"]):
# 		# BCs di riflesso in y
# 		if y[ii] <= tol*Dati["y_max"]:
# 			v[ii] = 1 / np.sqrt(2)
# 			u[ii] = 1 / np.sqrt(2)
# 		if y[ii] >= (1-tol)*Dati["y_max"]:
# 			v[ii] = -1 / np.sqrt(2)
# 			u[ii] = 1 / np.sqrt(2)
# 	return (u,v)

def PlotConfiguration(fig, Dati, x, y, u, v, kk, leaders):
	# NB: STO RI-SCRIVENDO - BISOGNA TROVARE IL MODO DI SOVRA-SCRIVERE

	plt.quiver(x, y, u, v, angles='xy', scale_units='xy')#, scale=0.2)
	xL, yL, uL, vL = leaders.getPosVel()
	plt.quiver(xL, yL, uL, vL, angles='xy', scale_units='xy', color='magenta')#, scale=0.2)
	plt.xlim([0, Dati["x_max"]])
	plt.ylim([0, Dati["y_max"]])
	#if Dati["Ostacolo"].startswith("Cerchio"):
	#	for x_center, y_center, radius in zip(Dati["x_o"],Dati["y_o"],Dati["r_o"]):
	#		circle = plt.Circle((x_center, y_center), radius, fill=False, color='red', linewidth=2)
	#		plt.gca().add_patch(circle)
	plt.title(kk)
	plt.show()


class PercorsoLeader:
	
    def __init__(self, Dati):
        
        self.kk = 0
        x_centro_leader, y_centro_leader = (0.5*Dati["init_x_max"], 0.5*Dati["init_y_max"])
        x_ampiezza_leader, y_ampiezza_leader = (0.01*Dati["x_max"], 0.01*Dati["y_max"])
        
        self.theta = np.pi/4.0
        self.x = np.random.rand(Dati["n_leaders"], 1) * 2*x_ampiezza_leader + x_centro_leader-x_ampiezza_leader
        self.y = np.random.rand(Dati["n_leaders"], 1) * 2*y_ampiezza_leader + y_centro_leader-y_ampiezza_leader
        
        self.u = np.cos(self.theta)
        self.v = np.sin(self.theta)

    def update(self, Dati):

        self.kk += 1
        self.theta = self.newtheta()
        
        self.u = np.cos(self.theta)
        self.v = np.sin(self.theta)
        
        self.x = self.x + self.u * Dati["velocita"]
        self.y = self.y + self.v * Dati["velocita"]
        
        return (self.x, self.y, self.u, self.v)

    def getPos(self): return (self.x, self.y)
    def getVel(self): return (self.u, self.v)
    def getTheta(self): return self.theta
    def getPosVel(self): return (self.x, self.y, self.u, self.v)

	# TOTALMENTE ARBITRARIO: FARSI GUIDARE
    def newtheta(self): return self.theta # + 0.001 * 2*np.pi

# def StochasticMatrixUndirected(n, p):
# 	"""
# 	Create random adjacency matrix and corresponding stochastic matrix
# 	for direction update.	
# 	Args:
# 		n: The size of the matrix.
# 		p: The probability threshold for creating edges (long-range interactions)
# 	Returns:
# 		A: The adjacency matrix.
# 		D: The degree matrix.
# 		F: The stochastic matrix.
# 	"""

# 	A = np.random.rand(n, n)
# 	A = (A + A.T) / 2
# 	A = (A > p).astype(int)

# 	D = np.zeros((n, n))
# 	for ii in range(n):
# 		A[ii, ii] = 0
# 		D[ii, ii] = np.sum(A[ii, :])

# 	I = np.eye(n)
# 	F = np.linalg.solve(I + D, I + A)

# 	return A, D, F

def CondizioneIniziale(Dati):
	n = Dati['n']

	# Posizionamento Casuale degli Individui al Tempo 0
	x = Dati['init_x_max'] * np.random.rand(n, 1)
	y = Dati['init_y_max'] * np.random.rand(n, 1)

	# Direzioni iniziali
	theta = Dati['init_theta_avg'] + 2 * Dati['init_theta_semispan'] * (np.random.rand(n, 1) - 0.5)
	u = np.cos(theta)
	v = np.sin(theta)

	return x, y, theta, u, v

@dataclass
class Params:
	n = 100 # Numero di elementi dello stormo
	w = 10  # Numero di leader
	T = 20 # Numero di istanti temporali simulati
	ps = 10 # plot ogni tot istanti (utile in sviluppo)
	x_max = 1280 # Lunghezza del dominio
	y_max = 720  # Altezza del dominio
	x0_max = 300
	y0_max = 150
	theta0_avg = 0
	theta0_var = np.pi/6
	v = 1  # Lunghezza di 1 passo temporale
	r = 10 # Raggio legame di vicinanza


class Engine:

	def __init__(self, args, player, flock, blocks):

		self.args = args
		self.player = player
		self.flock  = flock
		self.blocks = blocks
		self.n = self.args.n # Flock Members (not leader)
		self.w = self.args.w # Leader Weight

	@property
	def N(self):
		return self.n + self.w

	def build_flock(self):
		self.x = np.zeros((self.N),dtype=float)
		self.y = np.zeros((self.N),dtype=float)
		self.theta = np.zeros((self.N),dtype=float)
		
	def update(self, dt):

		# Retrieve Player coordinates
		self.x[:self.w] = np.zeros((self.w))+self.player.x
		self.y[:self.w] = np.zeros((self.w))+self.player.y
		self.x[self.w:] = np.array([f.x for f in self.flock])
		self.y[self.w:] = np.array([f.y for f in self.flock])

		# Compute new angle 
		theta = [self.player.dir_angle]*self.w + [f.dir_angle for f in self.flock]
		theta = self.move_step(theta)
		
		# AGGIUNGI COLLISIONI

		self.player.update(dt)
		for i,f in enumerate(self.flock):
			f.tar_angle = theta[self.w+i]
			f.update(dt)

	def close(self,ii,jj):
		dist = np.sqrt((self.x[ii] - self.x[jj])**2 + (self.y[ii] - self.y[jj])**2)
		return dist < self.args.r
	
	def norm(self, theta):
		return (theta + np.pi)%(2*np.pi) - np.pi

	def move_step(self, theta):

		# Matrix of connections
		A = np.zeros((self.N,self.N))
		for ii in range(self.N):
			for jj in range(ii + 1, self.N):
				if self.close(ii,jj):
					A[ii, jj] = 1
					A[jj, ii] = 1

		D = np.diag(np.sum(A, axis=1))
		I = np.eye(self.N)
		F = np.linalg.solve(I + D, I + A)

		noise = (np.random.rand(self.N, 1) - 0.5) * np.pi / 10
		theta = np.dot(F, theta) + noise

		return self.norm(theta)


def SimulaStormo(Dati):
	"""
	Simulates the flocking behavior of a group of agents.
	Args:
		Dati: A dictionary containing parameters for the simulation.
	Returns:	
		None
	"""

	n = Dati["n"]
	x_max = Dati["x_max"]
	y_max = Dati["y_max"]

	x, y, theta, u, v = CondizioneIniziale(Dati)

	# Setup leaders
	leaders = PercorsoLeader(Dati)
	x[0:Dati["n_leaders"]], y[0:Dati["n_leaders"]], u[0:Dati["n_leaders"]], v[0:Dati["n_leaders"]] = leaders.getPosVel()
	
	# # Spostamento degli Individui interni all'ostacolo
	# if Dati["Ostacolo"].startswith("Cerchio"):
	# 	for ii in range(n):
	# 		for jj in range(len(Dati["x_o"])):
	# 			if (x[ii] - Dati["x_o"][jj])**2 + (y[ii] - Dati["y_o"][jj])**2 <= Dati["r_o"][jj]**2:
	# 				x[ii] = 0
	# 				y[ii] = y_max * np.random.rand(1, 1)


	# Rappresentazione iniziale dello stormo
	fig_stormo = plt.figure()
	# xNOL, yNOL, uNOL, vNOL = [aa[Dati["n_leaders"]:-1] for aa in [x, y, u, v]]
	# PlotConfiguration(fig_stormo, Dati, xNOL, yNOL, uNOL, vNOL, 0, leaders)
	# plt.pause(0.1)
	# print('0 :', [np.mean(theta), np.mean(u), np.mean(v)])

	# Costruzione casuale del grafo con amicizia
	#A1, _, _ = StochasticMatrixUndirected(n,1-Dati["legame_lr"])

	# Iterazioni temporali
	for kk in range(Dati["tempo_max"]):
		#A = A1.copy() # Crea una copia di A1 per evitare modifiche indesiderate
		A = np.zeros((n,n))
		for ii in range(n):
			for jj in range(ii + 1, n):
				if np.sqrt((x[ii] - x[jj])**2 + (y[ii] - y[jj])**2) < Dati["r"]:
					A[ii, jj] = 1
					A[jj, ii] = 1

		D = np.diag(np.sum(A, axis=1))
		I = np.eye(n)
		F = np.linalg.solve(I + D, I + A)
		print(kk, ':', [np.mean(theta), np.mean(u), np.mean(v)])
		if kk % Dati["plot_stride"] == 0:
			xNOL, yNOL, uNOL, vNOL = [aa[Dati["n_leaders"]:-1] for aa in [x, y, u, v]]
			PlotConfiguration(fig_stormo, Dati, xNOL, yNOL, uNOL, vNOL, kk, leaders)

		# Aggiornamento della posizione
		leaders.update(Dati)
		x = x + u * Dati["velocita"]
		y = y + v * Dati["velocita"]
		#x, y = fix_BC(Dati, x, y)

		# # Collision detection with obstacles
		# if Dati["Ostacolo"].startswith("Cerchio"):
		# 	for jj in range(len(Dati["x_o"])):
		# 		if (x[ii] - Dati["x_o"][jj])**2 + (y[ii] - Dati["y_o"][jj])**2 < Dati["r_o"][jj]**2:
		# 			x[ii] = x[ii] - u[ii] * Dati["velocita"] # Adjust this value as needed
		# 			y[ii] = y[ii] - v[ii] * Dati["velocita"] # Adjust this value as needed
		# 			# You might want to add a bounce-back mechanism here, or other behavior when hitting an obstacle

		# Aggiornamento velocità
		theta = np.dot(F, theta) + (np.random.rand(n, 1) - 0.5) * np.pi / 10
		theta[0:Dati["n_leaders"]] = leaders.getTheta()

		# if Dati["Ostacolo"].startswith("Cerchio"):
		# 	for jj in range(len(Dati["x_o"])):
		# 		for ii in range(n):
		# 			if ((x[ii] - Dati["x_o"][jj])**2 + (y[ii] - Dati["y_o"][jj])**2) < (Dati["r_o"][jj] + 0.25)**2 and (x[ii] - Dati["x_o"][jj] < 0):
		# 				theta[ii] = np.arctan((y[ii] - Dati["y_o"][jj]) / (x[ii] - Dati["x_o"][jj]))
		# 				if theta[ii] > 0 and theta[ii] < np.pi / 2:
		# 					corr = -np.pi / 2
		# 				elif theta[ii]<0 and theta[ii] > -np.pi/2:
		# 					corr = np.pi/2
		# 				else:
		# 					corr = 0

		# 				theta[ii] = theta[ii] + corr

		# Aggiornamento della direzione
		theta = np.arctan(np.tan(theta));
		u = np.cos(theta)
		v = np.sin(theta)

		#v_plot = v.copy()
		#u, v = fix_BC_vel(Dati, x, y, u, v)

	print(f"centro dello stormo:\n\t({np.mean(x)}, {np.mean(y)})")
	print(f"ampiezza dello stormo (deviazione standard):\n\t{np.std(np.sqrt((x - np.mean(x))**2 + (y - np.mean(y))**2))}")

SimulaStormo(Dati)