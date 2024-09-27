from dataclasses import dataclass

@dataclass
class Globals:

    # PARAMETRI DA IMPOSTARE
    VERTICAL_CAMERA = 1     # ID della camera come letto da check_camera.py
    TRACKER_FLAG = True     # accende le webcam in INPUT (NECESSARIO per usare la mano)
    CAMERA_FLAG  = True     # accende le finestre per MOSTRARE QUANTO VISTO DALLA WEBCAM (se si vuole)
    SF = 1                  # scaling della finestra

    MAIN_CAMERA = 0

    # Parametri per rendering - NON modificare
    FPS = 30
    SW = 1280
    SH = 720

@dataclass
class Params:

    t_max: int = 60

    n: int = 100  # Numero di elementi dello stormo
    w: int = 1000  # Numero di leader
    r: int = 100  # Raggio legame di vicinanza
    r_player: float = 25.0
    r_npc: int = 20

    # Movement params
    speed: float = 60.0
    acc: float = 300.0
    rot: float = 5.0
    noise: float = 1.0

@dataclass
class Options:

    scen = 2
    diff = 1
    obst = 0
    mode = 1

glob = Globals()
args = Params()
opts = Options()

default_bird  = Params(n=200, w=500,  r=150, r_npc=20, r_player=1.25*20, speed=75, rot=5, noise=2)
default_fish  = Params(n=150, w=1000, r=100, r_npc=15, r_player=1.25*15, speed=50, rot=8, noise=3)
default_sheep = Params(n=50,  w=2000, r=150, r_npc=30, r_player=1.25*30, speed=50, rot=3, noise=1)
