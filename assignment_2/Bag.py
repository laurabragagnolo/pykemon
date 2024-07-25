from Items import Potion, Pokeball

class Bag:
    def __init__(self):
        self.bag = {}
            
    def addItem(self, item):
        if item.getName() in self.bag:
            self.bag[item.getName()] += 1
        else:
            self.bag[item.getName()] = 1
            
    def removeItem(self, item):
        if item.getName() in self.bag:
            if self.bag[item.getName()] > 0:
                self.bag[item.getName()] -= 1
            else:
                print("No more " + item.getName() +" in the bag.")
        else:
            print("No " + item.getName() +" in the bag.")
            
    def getItems(self):
        return self.bag.keys()
    
    def toString(self):
        string = ""
        for key in self.bag.keys():
            string += key + ": " + str(self.bag[key]) + ", "
        return string