from Items import Pokeball, Potion

class PokemonStore:
    def __init__(self):
        self.store = [Pokeball("Poké Ball"), Potion("Potion", 20)]
        
    def getStore(self):
        return self.store
    
    def sellItem(self, item):
        if item in self.store:
            print("Item " + item + "found.")
        else:
            print("Item " + item + " not found.")
            
    def fillTrainerBag(self, trainer, maxItems = 10):
        for i in range(0, maxItems):
            for item in self.store:
                trainer.bag.addItem(item)
            