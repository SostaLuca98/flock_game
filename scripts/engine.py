import numpy as np
import matplotlib.pyplot as plt

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

def fix_BC(Dati, x, y):
	for ii in range(Dati["n"]):
		# BCs periodiche in x
		if x[ii] < 0: x[ii] = x[ii] + Dati["x_max"]
		if x[ii] > Dati["x_max"]: x[ii] = x[ii] - Dati["x_max"]
		# BCs di riflesso in y
		if y[ii] < 0: y[ii] = 0
		if y[ii] > Dati["y_max"]: y[ii] = Dati["y_max"]
	return (x, y)

def fix_BC_vel(Dati, x, y, u, v):
	tol = 0.02
	for ii in range(Dati["n"]):
		# BCs di riflesso in y
		if y[ii] <= tol*Dati["y_max"]:
			v[ii] = 1 / np.sqrt(2)
			u[ii] = 1 / np.sqrt(2)
		if y[ii] >= (1-tol)*Dati["y_max"]:
			v[ii] = -1 / np.sqrt(2)
			u[ii] = 1 / np.sqrt(2)
	return (u,v)

def PlotConfiguration(fig, Dati, x, y, u, v, kk, leaders):
	# NB: STO RI-SCRIVENDO - BISOGNA TROVARE IL MODO DI SOVRA-SCRIVERE

	plt.quiver(x, y, u, v, angles='xy', scale_units='xy')#, scale=0.2)
	xL, yL, uL, vL = leaders.getPosVel()
	plt.quiver(xL, yL, uL, vL, angles='xy', scale_units='xy', color='magenta')#, scale=0.2)
	plt.xlim([0, Dati["x_max"]])
	plt.ylim([0, Dati["y_max"]])
	if Dati["Ostacolo"].startswith("Cerchio"):
		for x_center, y_center, radius in zip(Dati["x_o"],Dati["y_o"],Dati["r_o"]):
			circle = plt.Circle((x_center, y_center), radius, fill=False, color='red', linewidth=2)
			plt.gca().add_patch(circle)
	plt.title(kk)
	plt.show()

def Circle(x, y, r):
	"""
	Plots circles on a matplotlib plot.	
	Args:
		x: A list or array of x-coordinates of the circle centers.
		y: A list or array of y-coordinates of the circle centers.
		r: A list or array of radii of the circles.
	"""

	for i in range(len(r)):
		circle = plt.Circle((x[i], y[i]), r[i], fill=False, color='g', linewidth=2)
		plt.gca().add_patch(circle)
	plt.axis('scaled')

class PercorsoLeader:
	
    def __init__(self, Dati):
        
        self.kk = 0
        x_centro_leader, y_centro_leader = (0.5*Dati["init_x_max"], 0.5*Dati["init_y_max"])
        x_ampiezza_leader, y_ampiezza_leader = (0.01*Dati["x_max"], 0.01*Dati["y_max"])
        
        self.theta = np.pi/4.0
        self.x = np.random.rand(Dati["n_leaders"], 1) * 2*x_ampiezza_leader + x_centro_leader-x_ampiezza_leader
        self.y = np.random.rand(Dati["n_leaders"], 1) * 2*y_ampiezza_leader + y_centro_leader-y_ampiezza_leader
        assert(self.x.size == Dati["n_leaders"] and self.y.size == Dati["n_leaders"])
        
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

def StochasticMatrixUndirected(n, p):
	"""
	Create random adjacency matrix and corresponding stochastic matrix
	for direction update.	
	Args:
		n: The size of the matrix.
		p: The probability threshold for creating edges (long-range interactions)
	Returns:
		A: The adjacency matrix.
		D: The degree matrix.
		F: The stochastic matrix.
	"""

	A = np.random.rand(n, n)
	A = (A + A.T) / 2
	A = (A > p).astype(int)

	D = np.zeros((n, n))
	for ii in range(n):
		A[ii, ii] = 0
		D[ii, ii] = np.sum(A[ii, :])

	I = np.eye(n)
	F = np.linalg.solve(I + D, I + A)

	return A, D, F

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
	import pdb; pdb.set_trace()

	# Spostamento degli Individui interni all'ostacolo
	if Dati["Ostacolo"].startswith("Cerchio"):
		for ii in range(n):
			for jj in range(len(Dati["x_o"])):
				if (x[ii] - Dati["x_o"][jj])**2 + (y[ii] - Dati["y_o"][jj])**2 <= Dati["r_o"][jj]**2:
					x[ii] = 0
					y[ii] = y_max * np.random.rand(1, 1)


	# Rappresentazione iniziale dello stormo
	fig_stormo = plt.figure()
	xNOL, yNOL, uNOL, vNOL = [aa[Dati["n_leaders"]:-1] for aa in [x, y, u, v]]
	PlotConfiguration(fig_stormo, Dati, xNOL, yNOL, uNOL, vNOL, 0, leaders)
	plt.pause(0.1)
	print('0 :', [np.mean(theta), np.mean(u), np.mean(v)])

	# Costruzione casuale del grafo con amicizia
	A1, _, _ = StochasticMatrixUndirected(n,1-Dati["legame_lr"])

	# Iterazioni temporali
	for kk in range(Dati["tempo_max"]):
		A = A1.copy() # Crea una copia di A1 per evitare modifiche indesiderate
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
		x, y = fix_BC(Dati, x, y)

		# Collision detection with obstacles
		if Dati["Ostacolo"].startswith("Cerchio"):
			for jj in range(len(Dati["x_o"])):
				if (x[ii] - Dati["x_o"][jj])**2 + (y[ii] - Dati["y_o"][jj])**2 < Dati["r_o"][jj]**2:
					x[ii] = x[ii] - u[ii] * Dati["velocita"] # Adjust this value as needed
					y[ii] = y[ii] - v[ii] * Dati["velocita"] # Adjust this value as needed
					# You might want to add a bounce-back mechanism here, or other behavior when hitting an obstacle

		# Aggiornamento velocità
		theta = np.dot(F, theta) + (np.random.rand(n, 1) - 0.5) * np.pi / 10
		theta[0:Dati["n_leaders"]] = leaders.getTheta()

		if Dati["Ostacolo"].startswith("Cerchio"):
			for jj in range(len(Dati["x_o"])):
				for ii in range(n):
					if ((x[ii] - Dati["x_o"][jj])**2 + (y[ii] - Dati["y_o"][jj])**2) < (Dati["r_o"][jj] + 0.25)**2 and (x[ii] - Dati["x_o"][jj] < 0):
						theta[ii] = np.arctan((y[ii] - Dati["y_o"][jj]) / (x[ii] - Dati["x_o"][jj]))
						if theta[ii] > 0 and theta[ii] < np.pi / 2:
							corr = -np.pi / 2
						elif theta[ii]<0 and theta[ii] > -np.pi/2:
							corr = np.pi/2
						else:
							corr = 0

						theta[ii] = theta[ii] + corr

		# Aggiornamento della direzione
		theta = np.arctan(np.tan(theta));
		u = np.cos(theta)
		v = np.sin(theta)

		v_plot = v.copy()
		u, v = fix_BC_vel(Dati, x, y, u, v)

	print(f"centro dello stormo:\n\t({np.mean(x)}, {np.mean(y)})")
	print(f"ampiezza dello stormo (deviazione standard):\n\t{np.std(np.sqrt((x - np.mean(x))**2 + (y - np.mean(y))**2))}")

SimulaStormo(Dati)