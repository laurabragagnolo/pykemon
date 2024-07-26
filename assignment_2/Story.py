from Battle import Battle, RESULTS
from PokemonCenter import PokemonCenter
from PokemonStore import PokemonStore
import random
import Pokedex
import copy

class Story():
    def __init__(self, trainer):
        print("Start the story.")
        self.trainer = trainer
        self.pokemonCenter = PokemonCenter()
        self.pokemonStore = PokemonStore()
        
    def askWhatDo(self):
        action = 0 
        while not action == 6:
            print("What do you want to do?")
            print("1. Go to the Pokemon Center.")
            print("2. Go to the Pokemon Store.")
            print("3. Go to the Wild.")
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
        print(self.trainer.getSquad().toString())
        
    def showBag(self):
        print("Your bag contains: ")
        print(self.trainer.getBag().toString())        
        
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
            opponent_id = random.choice(list(Pokedex.pokedex.keys()))
            opponent = copy.deepcopy(Pokedex.pokedex[opponent_id])
            print("A " + opponent.getName() + " appeared!")
            battle = Battle(self.trainer, opponent)
            a = battle.runBattle() # gestire se perde del tutto o se cattura il pokemon
            if a == RESULTS[2]:
                print('You have been defeated. You go to the pokemon center')
                self.pokemonCenter.healPokemons(self.trainer.getSquad().getPokemons())
            elif a == RESULTS[4]:
                self.trainer.addPokemon(opponent)