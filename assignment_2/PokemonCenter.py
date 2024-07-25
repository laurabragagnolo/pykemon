from Character import Character

class PokemonCenter:
    def __init__(self):
        pass
    
    def healPokemons(self, pokemons):
        for i in range(0, len(pokemons)):
            pokemons[i].restoreC_HP()
            pokemons[i].restorePP()

        
    def toString(self):
        string = ""
        for i in range(0, len(self.pokemons)):
            string += self.pokemons[i].getName() + ", "
        return string