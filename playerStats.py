from weaponsList import weaponsList
from utils import findWeapon

playersDic = {}

class Player:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.maxHealth = 20
        self.health = self.maxHealth
        self.kit = None
        self.weapon = findWeapon("hand")
    
    def reset(self):
        self.__init__(id=self.id, name=self.name)
