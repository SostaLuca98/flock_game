from dataclasses import dataclass

@dataclass
class Params:
    TRACKER_FLAG = False
    CAMERA_FLAG  = False

    # Parametri per rendering - modificare solo SF
    FPS = 30
    SW = 1280
    SH = 720
    SF = 1

    n = 200  # Numero di elementi dello stormo
    w = 1000  # Numero di leader
    r = 100  # Raggio legame di vicinanza
    r_player = 25
    r_npc = 20

    # Movement params
    speed = 60
    acc = 300
    rot = 5


@dataclass
class Options:
    scen = 0
    diff = 0
    obst = 1
    mode = 0

args = Params()
options = Options()