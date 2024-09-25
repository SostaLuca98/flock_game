from dataclasses import dataclass

@dataclass
class Params:
    TRACKER_FLAG = True
    CAMERA_FLAG  = True

    n = 200  # Numero di elementi dello stormo
    w = 1000  # Numero di leader
    r = 100  # Raggio legame di vicinanza
    r_player = 25
    r_npc = 20

    # Movement params
    speed = 50
    acc = 300
    rot = 5


    # Parametri per rendering - modificare solo SF
    FPS = 30
    SW = 1280
    SH = 720
    SF = 1.2

# Params va usato per indicare lo scenario? (Mare, Rondini, ecc)

args = Params()
