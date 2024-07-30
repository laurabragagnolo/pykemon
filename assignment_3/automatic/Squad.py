from Character import Character

class Squad:
    def __init__(self):
        self.squad = []
        
    def addCharacter(self, character):
        if len(self.squad) >= 6:
            print("Squad is full. You cannot add more Pokemons.")
            return False
        else:
            self.squad.append(character)
            return True
            
    def getPokemons(self):
        return self.squad
        
    def __str__(self):
        string = ""
        for i in range(0, len(self.squad)):
            string += str(self.squad[i]) + "\n "
        string = string[:-2]
        return string
    
    def __repr__(self):
        string = ""
        for i in range(0, len(self.squad)):
            string += str(self.squad[i]) + "\n "
        string = string[:-2]
        return string