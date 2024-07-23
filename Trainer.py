

class Trainer:
    def __init__(self):
        self.name = ""
        self.pokemon = []
        self.items = []
        
    def __init__(self, name, pokemon, items):
        self.name = name
        
        if len(pokemon) > 6:
            print("You can only have 6 pokemon in your party.")
        else:
            self.pokemon = pokemon
            
        self.items = {}
    
    def __init__(self, name):
        self.name = name
        self.pokemon = []
        self.items = []
        
    def addPokemon(self, pokemon):
        if len(self.pokemon) < 6:
            self.pokemon.append(pokemon)
        else:
            print("You can only have 6 pokemon in your party.")
            
    def removePokemon(self, pokemon):
        if len(self.pokemon) <= 0:
            print("You have no pokemon in your party.")
        else:
            for i in range(len(self.pokemon)):
                if self.pokemon[i].getPokedexId() == pokemon.getPokedexId():
                    self.pokemon.pop(i)
                    break
                else:
                    print("You do not have a pokemon name " + pokemon.getName() + " in your party and id: ." + pokemon.getPokedexId())
                    
    def toString(self):
        string = "Name: " + self.name + "\nPokemon: "
        for i in range(0, len(self.pokemon)):
            string += "\n          " + self.pokemon[i].toString()
        return string