from Character import Character

class Squad:
    def __init__(self):
        self.squad = []
        
    def addCharacter(self, character):
        if len(self.squad) >= 6:
            print("Squad is full.")
        else:
            self.squad.append(character)
        
    def toString(self):
        string = ""
        for i in range(0, len(self.squad)):
            string += self.squad[i].toString() + ", "
        return string