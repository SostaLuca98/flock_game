from dataclasses import dataclass
import json, os

@dataclass
class Globals:

    # PARAMETRI DA IMPOSTARE
    
    MAIN_CAMERA     = None  # ID della camera principale 
    VERTICAL_CAMERA = None  # ID della camera come letto da check_camera.py
    
    TRACKER_FLAG = None     # accende le webcam in INPUT (NECESSARIO per usare la mano)
    CAMERA_FLAG  = None     # accende le finestre per MOSTRARE QUANTO VISTO DALLA WEBCAM (se si vuole)
    
    INFLUENCE = None        # raggio di influenza iniziale [binary, smooth]
    SF = None               # scaling della finestra

    # Parametri per rendering - NON modificare
    FPS = 30
    SW = 1280
    SH = 720

    # Metodo per aggiornare i parametri globali
    def update(self, params: dict):
        for k, v in params.items():
            if hasattr(self, k):
                setattr(self, k, v)

@dataclass
class Levels:

    # Generic params
    name:  str = "Default"
    t_max: int = 60
    pacman_x: bool = True
    pacman_y: bool = True

    # Flock params
    n: int = 100  # Numero di elementi dello stormo
    w: int = 1000 # Numero di leader
    r_influence: float = 100.0 # Raggio legame di vicinanza
    r_player:    float = 25.0
    r_npc:       float = 20.0

    # Movement params
    speed: float = 60.0
    acc: float = 300.0
    rot: float = 5.0
    noise: float = 0.8

    # Blocks
    blocks: tuple = None # (x,y,r)
    target: tuple = None # (x,y,r)

@dataclass
class Options:

    scen = 2
    diff = 1
    obst = 0
    mode = 0
    temp = 2

glob = Globals()
with open("./config.json", "r") as f:
    glob_params = json.load(f)
glob.update(glob_params)

opts = Options()
levels = Levels()

blocks_human = (( 340, 200, 50), ( 340, 350, 50),
                ( 340, 500, 50), ( 280, 275, 50),
                ( 280, 425, 50), ( 580, 175, 50),
                ( 680, 530, 50), (1140, 190, 50))
blocks_other = (( 500, 200, 50), ( 700, 400, 50))
target_human = ( 70, 360, 75)
target_other = (100, 500, 75)

default_bird  = Levels(pacman_x= True, pacman_y= True, blocks=blocks_other, target=target_other, n=200, w=500,  r_influence=150, r_npc=20, r_player=1.25*20, speed=75, rot=5, noise=2)
default_fish  = Levels(pacman_x= True, pacman_y=False, blocks=blocks_other, target=target_other, n=150, w=1000, r_influence=100, r_npc=15, r_player=1.25*15, speed=50, rot=8, noise=2.5)
default_human = Levels(pacman_x=False, pacman_y=False, blocks=blocks_human, target=target_human, n=100, w=1200, r_influence=100, r_npc=40, r_player=1.25*40, speed=65, rot=3, noise=2)
default_abstr = Levels(pacman_x= True, pacman_y= True, blocks=blocks_other, target=target_other, n=200, w=500,  r_influence=150, r_npc=30, r_player=1.25*30, speed=50, rot=3, noise=1)