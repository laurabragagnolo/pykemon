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
        df_to_save = []
        for i in range(0, n+1):
            c_to_save = dict()
            opponent_id = random.choice(list(self.pokedex['Pokemon Number']))
            opponent = copy.deepcopy(self.pokedex.loc[self.pokedex['Pokemon Number'] == opponent_id]['Pokemon'].values[0])
            opponent.setLevel(random.randint(1, 20))

            chooseRandomMoves(opponent, self.MN)
            print(len(self.trainer.getSquad().getPokemons()))   
            battle = Battle(self.trainer.getSquad().getPokemons()[0], opponent, self.type_effectiveness)
            battle_df = battle.runBattle() 
            df_to_save.append(battle_df)

            self.pokemonCenter.healPokemons(self.trainer.getSquad().getPokemons())

        data = pd.concat(df_to_save, ignore_index=True)
        
        return data
    
    def askWhatDo(self):
        action = 0 
        while not action == 6:
            print("What do you want to do?")
            print("1. Go to the Pokemon Center.")
            print("2. Go to the Pokemon Store.")
            print("3. Explore.")
            print("4. See your pokemons.")
            print("5. See your bag.")
            print("6. Exit.")
            
            action = int(input("Action selected: "))
            
            if action not in range(1, 7):
                print("Invalid action.")
                continue
            
            if action == 1:
                self.goToPokemonCenter()
            elif action == 2:
                self.goToPokemonStore()
            elif action == 3:
                self.explore()
            elif action == 4:
                self.showPokemons()
            elif action == 5:
                self.showBag()
            else:
                print("Goodbye.")
    
    def showPokemons(self):
        print("Your pokemons are: ")
        print(self.trainer.getSquad())
        
    def showBag(self):
        print("Your bag contains: ")
        print(self.trainer.getBag())        
        
    def goToPokemonStore(self):
        print("Welcome to the Pokemon Store.")
        print("What do you want to buy?")
        items = self.pokemonStore.getStore()
        for i, item in enumerate(items):
            print(str(i) + ": " + item.getName())
        print(str(i+1) + ": Fill the bag with items already present in the bag.")
        print(str(i+2) + ": Exit")
        
        action = int(input("Action selected: "))
        
        if action == i+2:
            return
        
        if action == i + 2:
            items_trainer = self.trainer.getBag().getItems()
            for item in items_trainer:
                self.pokemonStore.fillTrainerBag(self.trainer, item)
        else:
            self.trainer.getBag().addItem(items[action])
        
    def goToPokemonCenter(self):
        self.pokemonCenter.healPokemons(self.trainer.getSquad().getPokemons())
        
    def explore(self):
        randomProb = random.random()
        if randomProb < 0.8:
            print("You found a wild pokemon!")
            opponent_id = random.choice(list(self.pokedex['Pokemon Number']))
            opponent = copy.deepcopy(self.pokedex.loc[self.pokedex['Pokemon Number'] == opponent_id]['Pokemon'].values[0])
            chooseRandomMoves(opponent, self.MN)
            print("A " + opponent.getName() + " appeared!")
            battle = Battle(self.trainer.getSquad().getPokemons(), opponent, self.type_effectiveness)
            df_battle = battle.runBattle_ml()

            result = df_battle['result'].values[0]
            
            if result == RESULTS[2]:
                print('You have been defeated. You go to the pokemon center')
                self.pokemonCenter.healPokemons(self.trainer.getSquad().getPokemons())
            elif result == RESULTS[4]:
                self.trainer.addPokemon(opponent)

        