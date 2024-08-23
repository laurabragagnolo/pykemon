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
                    
    def __str__(self):
        string = "Name: " + self.name
        
        string += "\nPokemon Team: " + str(self.squad)
        
        string += "\nBag: " + str(self.bag)
        
        return string
    
    def __repr__(self):
        string = "Name: " + self.name
        
        string += "\nPokemon Team: " + str(self.squad)
        
        string += "\nBag: " + str(self.bag)
        
        return string