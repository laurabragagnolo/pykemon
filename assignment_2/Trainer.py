from Bag import Bag
from Squad import Squad

class Trainer:
    def __init__(self):
        self.name = ""
        self.squad = Squad()
        self.bag = Bag()
        
    def __init__(self, name):
        self.name = name
        self.squad = Squad()
        self.bag = Bag()
        
    def addPokemon(self, pokemon):
        return self.squad.addCharacter(pokemon)
        
    def getSquad(self):
        return self.squad
    
    def getBag(self):
        return self.bag
                    
    def toString(self):
        string = "Name: " + self.name
        
        string += "\nPokemon Team: " + self.squad.toString()
        
        string += "\nBag: " + self.bag.toString()
        
        return string