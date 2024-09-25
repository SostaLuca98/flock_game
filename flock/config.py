from dataclasses import dataclass

@dataclass
class Params:
    n = 200  # Numero di elementi dello stormo
    w = 1000  # Numero di leader
    r = 150  # Raggio legame di vicinanza
    r_player = 25
    r_npc = 20
    speed = 50
