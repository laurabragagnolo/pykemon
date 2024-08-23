from Battle import Battle, RESULTS
from PokemonCenter import PokemonCenter
from PokemonStore import PokemonStore
import random
from utils import *
import copy

class Story():
    def __init__(self, trainer, pokedex, MN, type_effectiveness):
        # print("Start the story.")
        self.trainer = trainer
        self.pokemonCenter = PokemonCenter()
        self.pokemonStore = PokemonStore()
        self.pokedex = pokedex
        self.MN = MN
        self.type_effectiveness = type_effectiveness
        
    def automaticExploration(self, n):
        to_save = []
        for i in range(0, n+1):
            opponent_id = random.choice(list(self.pokedex['Pokemon Number']))
            opponent = copy.deepcopy(self.pokedex.loc[self.pokedex['Pokemon Number'] == opponent_id]['Pokemon'].values[0])
            opponent.setLevel(random.randint(1, 20))

            chooseRandomMoves(opponent, self.MN)

            battle = Battle(self.trainer.getSquad().getPokemons()[0], opponent, self.type_effectiveness)
            data  = battle.runBattle() 

            self.pokemonCenter.healPokemons(self.trainer.getSquad().getPokemons())

            to_save.append(data)

        
        # Convert to pandas DataFrame
        df = pd.DataFrame(to_save)
        # print("Goodbye.")
        
        return df
        