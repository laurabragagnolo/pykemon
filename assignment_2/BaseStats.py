class BaseStats:
    def __init__(self, hp, attack, defense, speed, special):
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.special = special
        
    def getHP(self):
        return self.hp
    
    def getAttack(self):
        return self.attack
    
    def getDefense(self):
        return self.defense
    
    def getSpeed(self):
        return self.speed
    
    def getSpecial(self):
        return self.special
    
    def setHP(self, hp):
        self.hp = hp
        
    def setAttack(self, attack):
        self.attack = attack
        
    def setDefense(self, defense):
        self.defense = defense
        
    def setSpeed(self, speed):
        self.speed = speed
        
    def setSpecial(self, special):
        self.special = special
        
    def toString(self):
        return "HP: " + str(self.hp) + " Attack: " + str(self.attack) + " Defense: " + str(self.defense) + " Speed: " + str(self.speed) + " Special: " + str(self.special)