import random

class Item:
    def __init__(self, name):
        self.name = name
        
    def getName(self):
        return self.name
    
    
class Potion(Item):
    def __init__(self, name, hp):
        super().__init__(name)
        self.hp = hp
        
    def getHP(self):
        return self.hp
    
    def use(self, pokemon):
        if pokemon.getC_HP() == pokemon.getBaseStats().getHP():
            print(pokemon.getName() + " is already at full health.")
            return False
        else:
            p_c_hp = pokemon.getC_HP()
            p_hp = pokemon.getBaseStats().getHP()
            if p_c_hp + self.hp > p_hp:
                pokemon.addC_HP(p_hp - p_c_hp)
                print(pokemon.getName() + " has recovered " + str(p_hp - p_c_hp) + " HP.")
            else:
                pokemon.addC_HP(self.hp)
                print(pokemon.getName() + " has recovered " + str(self.hp) + " HP.")
            return True
                
    def getName(self):
        return super().getName()
    
    def __eq__(self, item):
        return self.getName() == item.getName()
    
    def __hash__(self):
        return hash((super().getName(), self.hp))
    
class Pokeball(Item):
    def __init__(self, name):
        super().__init__(name)
        
    def getName(self):
        return super().getName()
    
    def use(self, pokemon):
        randomProb = random.random()
        catchProbability = 1.0 - (pokemon.getC_HP() / pokemon.getBaseStats().getHP())
        if randomProb < catchProbability:
            print(pokemon.getName() + " has been caught.")
            return True
        else:
            print(pokemon.getName() + " has escaped from the " + self.getName() + ".")
            return False
        
    def __eq__(self, item):
        return self.getName() == item.getName()
        
    def __hash__(self):
        return hash(super().getName())