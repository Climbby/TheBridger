class Player:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.maxHealth = 20
        self.health = self.maxHealth
        self.kit = None
        self.weapon = "hand"
