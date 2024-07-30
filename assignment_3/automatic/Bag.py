from Items import Potion, Pokeball

class Bag:
    def __init__(self):
        self.bag = {}
            
    def addItem(self, item):
        if item in self.bag.keys():
            self.bag[item] += 1
        else:
            self.bag[item] = 1
            
    def removeItem(self, item):
        if item in self.bag.keys():
            if self.bag[item] > 0:
                self.bag[item] -= 1
            else:
                print("No more " + item.getName() +" in the bag.")
        else:
            print("No " + item.getName() +" in the bag.")
            
    def getItems(self):
        return self.bag
    
    def __str__(self):
        string = ""
        for key in self.bag.keys():
            string += key.getName() + ": " + str(self.bag[key]) + ", "
        string = string[:-2]
        return string
    
    def __repr__(self):
        string = ""
        for key in self.bag.keys():
            string += key.getName() + ": " + str(self.bag[key]) + ", "
        string = string[:-2]
        return string