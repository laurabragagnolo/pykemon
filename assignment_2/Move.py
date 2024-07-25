class Move:
    def __init__(self, name, type_, category, power, accuracy, pp):
        self.name = name
        self.type = type_
        self.category = category
        self.power = power
        self.accuracy = accuracy
        self.pp = pp
        self.max_pp = pp
        
    def getName(self):
        return self.name
    
    def getType(self):
        return self.type
    
    def getCategory(self):
        return self.category
    
    def getPower(self):
        return self.power
    
    def getAccuracy(self):
        return self.accuracy
    
    def getPP(self):
        return self.pp
    
    def getMaxPP(self):
        return self.max_pp
    
    def setPP(self, pp):
        self.pp = pp
        
    def toString(self):
        return "          Name: " + self.name + " Type: " + self.type + " Category: " + self.category + " Power: " + str(self.power) + " Accuracy: " + str(self.accuracy) + " PP: " + str(self.pp)
    