from Character import Character
from Items import Potion, Pokeball
import random

RESULTS = {1 : "Attacker wins", 2 : "Defender wins", 3 : "Trainer run away", 4 : "Wild pokemon caught", 5 : "Battle continues", 6 : "Go back"}

class Battle:
    def __init__(self, trainer, wild_pokemon):
        self.trainer = trainer
        self.wild_pokemon = wild_pokemon
        pokemons = trainer.getSquad().getPokemons()
        for pokemon in pokemons:
            if pokemon.getC_HP() > 0:
                self.active_pokemon = pokemon
                break
        
    def runBattle(self):
        # start with the choice of the trainer
        res = RESULTS[5]
        while res == RESULTS[5] or res == RESULTS[6]:
            if res == RESULTS[5]:
                print(self.active_pokemon.getName() + " HP: " + str(self.active_pokemon.getC_HP()))
                print(self.wild_pokemon.getName() + " HP: " + str(self.wild_pokemon.getC_HP()))
            
            res = self.turn()
            if res == RESULTS[2]: # pokemon active is dead
                pokemonFromSquad = self.trainer.getSquad().getPokemons()
                available_pokemon = []
                map_to_squad = []
                for i,opt in enumerate(pokemonFromSquad):
                    if opt.getC_HP() > 0:
                        available_pokemon.append(opt)
                        map_to_squad.append(i)
                
                if(len(available_pokemon) == 0):
                    print("You have no more pokemon left")
                    return RESULTS[2]
                else:
                    print("Choose another pokemon to continue the battle")
                    for i, opt in enumerate(available_pokemon):
                        print(str(i) + ": " + opt.getName())
                    choice = int(input("Pokemon choice: "))
                    self.active_pokemon = self.trainer.getSquad().getPokemons()[map_to_squad[choice]]
                    res = RESULTS[5]
            elif res == RESULTS[4]: # pokemon caught
                print("You caught the wild pokemon")
                return RESULTS[4]
            elif res == RESULTS[1]:
                print("You defeated the wild pokemon")
                return RESULTS[1]
                
    
    def turn(self):
        print("What would you like to do?")
        print("1: Fight\n2: Change pokemon\n3: Use item\n4: Run")
        action = int(input("Action selected: "))
        while True:
            if action == 1:
                res = self.fight()
                return res
            elif action == 2:
                res = self.changePokemon()
                if res == RESULTS[5]:
                    idx_wild_move = self.getIdxWildPokemonMove()
                    self.wild_pokemon.useMove(idx_wild_move, self.active_pokemon)
                    if self.active_pokemon.getC_HP() <= 0:
                        self.active_pokemon.setC_HP(0)
                        res = RESULTS[2]
                return res
            elif action == 3: 
                res = self.useItem()
                if res == RESULTS[5]:
                    idx_wild_move = self.getIdxWildPokemonMove()
                    self.wild_pokemon.useMove(idx_wild_move, self.active_pokemon)
                    if self.active_pokemon.getC_HP() <= 0:
                        self.active_pokemon.setC_HP(0)
                        res = RESULTS[2]
                return res
            elif action == 4:
                res = self.escape()
                if res == RESULTS[5]:
                    idx_wild_move = self.getIdxWildPokemonMove()
                    self.wild_pokemon.useMove(idx_wild_move, self.active_pokemon)
                    if self.active_pokemon.getC_HP() <= 0:
                        res = RESULTS[2]
                return res
            else:
                print("Invalid action")
                action = int(input("Action selected: "))
  
    def fight(self):
        # ask to the user which move he wants to use
        print(self.active_pokemon.getName() + " can use:")
        # take the move with enough PP
        all_moves = self.active_pokemon.getMoves()
        available_moves = []
        map_to_moves = []
        for i in range(0, len(all_moves)):
            if all_moves[i].getPP() > 0:
                available_moves.append(all_moves[i])
                map_to_moves.append(i)
                
        for i, opt in enumerate(available_moves):
            print(str(i) + ": " + opt.getName() + " PP: " + str(opt.getPP()) + "/" + str(opt.getMaxPP()))
        print(str(i+1) + ": go back")
            
        choice = int(input("Move choice: "))
        if choice == i+1:
            return RESULTS[6]
        idx_attacker_move = map_to_moves[choice]
        
        # same for wild pokemon
        idx_wild_move = self.getIdxWildPokemonMove()
        
        # check the velocity of the pokemon
        if self.active_pokemon.getBaseStats().getSpeed() > self.wild_pokemon.getBaseStats().getSpeed():
            self.active_pokemon.useMove(idx_attacker_move, self.wild_pokemon)
            if self.wild_pokemon.getC_HP() > 0:
                self.wild_pokemon.useMove(idx_wild_move, self.active_pokemon)
            else:
                return RESULTS[1]
        else:
            self.wild_pokemon.useMove(idx_wild_move, self.active_pokemon)
            if self.active_pokemon.getC_HP() > 0:
                self.active_pokemon.useMove(idx_attacker_move, self.wild_pokemon)
            else:
                self.active_pokemon.setC_HP(0)
                return RESULTS[2]
            
        if self.active_pokemon.getC_HP() <= 0:
            self.active_pokemon.setC_HP(0)
            return RESULTS[2]
        elif self.wild_pokemon.getC_HP() <= 0:
            return RESULTS[1]
            
        return RESULTS[5]
    
    def getIdxWildPokemonMove(self):
        all_moves = self.wild_pokemon.getMoves()
        map_to_moves = []
        available_moves = []
        for i in range(0, len(all_moves)):
            if all_moves[i].getPP() > 0:
                map_to_moves.append(i)
                available_moves.append(all_moves[i])
        
        choice = random.randint(0, len(available_moves) - 1)
        idx_wild_move = map_to_moves[choice]
        
        return idx_wild_move
    
    def escape(self):
        random_number = random.random()
        if random_number < 0.6: 
            print("You run away")
            return RESULTS[3]
        else:
            print("You cannot run away")
            return RESULTS[5]
        
    def useItem(self):
        print("What item would you like to use?")
        bag = self.trainer.getBag()
        items = bag.getItems()
        for i, opt in enumerate(items):
            print(str(i) + ": " + opt.getName())
        print(str(i+1) + ": go back")
            
        choice = int(input("Item choice: "))
        if choice == i+1:
            return RESULTS[6]
        item = list(items.keys())[choice]
        
        if item.getName() == "Potion": #TODO generalize to who
            pokemons = self.trainer.getSquad().getPokemons()
            print("Available pokemon for the usage of the " + item.getName() + ":")
            available_pokemon = []
            map_to_squad = []
            for i in range(0, len(pokemons)):
                pokemon = pokemons[i]
                if pokemon.getC_HP() < pokemon.getBaseStats().getHP() and pokemon.getC_HP() > 0:
                    available_pokemon.append(pokemon)
                    map_to_squad.append(i)
            
            i = 0        
            for i, opt in enumerate(available_pokemon):
                print(str(i) + ": " + opt.getName())
            print(str(i+1) + ": go back")
                
            choice = int(input("Pokemon choice: "))
            if choice == i+1:
                return RESULTS[6]
            
            choosen_pokemon = pokemons[map_to_squad[choice]]
            
            used_potion = item.use(choosen_pokemon)
            if used_potion:
                bag.removeItem(item)
            else:
                return RESULTS[6]
        elif item.getName() == "Poké Ball":
            res = item.use(self.wild_pokemon)
            bag.removeItem(item)
            if res:
                return RESULTS[4]
            
        return RESULTS[5]
    
    def changePokemon(self):
        print("Available pokemon:")
        pokemonFromSquad = self.trainer.getSquad().getPokemons()
        available_pokemon = []
        map_to_squad = []
        
        for i in range(0, len(pokemonFromSquad)):
            if not pokemonFromSquad[i].getName() == self.active_pokemon.getName():
                if pokemonFromSquad[i].getC_HP() > 0:
                    available_pokemon.append(pokemonFromSquad[i])
                    map_to_squad.append(i)
        
        
        for i, opt in enumerate(available_pokemon):
            print(str(i) + ": " + opt.getName())
        print(str(i+1) + ": go back")
            
        choice = int(input("Pokemon choice: "))
        if choice == i+1:
            return RESULTS[6]
        
        self.active_pokemon = self.trainer.getSquad().getPokemons()[map_to_squad[choice]]
        
        return RESULTS[5]
            
