from Character import Character
from Items import Potion, Pokeball
import random

RESULTS = {1 : "Attacker wins", 2 : "Defender wins", 3 : "Trainer run away", 4 : "Wild pokemon caught", 5 : "Battle continues"}

class Battle:
    def __init__(self, trainer, wild_pokemon):
        self.trainer = trainer
        self.wild_pokemon = wild_pokemon
        self.active_pokemon = trainer.getSquad()[0]
        
    def runBattle(self):
        # start with the choice of the trainer
        res = RESULTS[5]
        while res == RESULTS[5]:
            res_trainer = self.turn()
            if res_trainer == RESULTS[2]: # TODO case with no pokemon left
                print("Choose another pokemon to continue the battle")
                
            
            
            
        # the motion of the trainer if is to attack depends on the velocity of the pokemon otherwise to it first
        # check the different stages
    
    def turn(self):
        print("What would you like to do?")
        print("1: Fight\n2: Change pokemon\n3: Use item\n4: Run")
        action = int(input("Action selected: "))
        while True:
            if action == 1:
                res = self.fight()
                break
            elif action == 2:
                res = self.changePokemon()
                idx_wild_move = self.getIdxWildPokemonMove()
                self.wild_pokemon.useMove(self.wild_pokemon.getMoves()[idx_wild_move].getName(), self.active_pokemon)
                if self.active_pokemon.getC_HP() > 0:
                    res = RESULTS[2]
            elif action == 3:
                res = self.useItem()
                idx_wild_move = self.getIdxWildPokemonMove()
                self.wild_pokemon.useMove(self.wild_pokemon.getMoves()[idx_wild_move].getName(), self.active_pokemon)
                if self.active_pokemon.getC_HP() > 0:
                    res = RESULTS[2]
                break
            elif action == 4:
                res = self.escape()
                if res == RESULTS[5]:
                    self.wild_pokemon.useMove(self.wild_pokemon.getMoves()[idx_wild_move].getName(), self.active_pokemon)
                    if self.active_pokemon.getC_HP() > 0:
                        res = RESULTS[2]
                break
            else:
                print("Invalid action")
                action = int(input("Action selected: "))
        return res
  
    def fight(self):
        # ask to the user which move he wants to use
        print("Available moves:")
        # take the move with enough PP
        all_moves = self.active_pokemon.getMoves()
        available_moves = []
        map_to_moves = []
        for i in range(0, len(all_moves)):
            if all_moves[i].getPP() > 0:
                available_moves.append(all_moves[i])
                map_to_moves.append(i)
                
        for i, opt in enumerate(available_moves):
            print(str(i) + ": " + opt.getName())
            
        choice = int(input("Move choice: "))
        idx_attacker_move = map_to_moves[choice]
        
        # same for wild pokemon
        idx_wild_move = self.getIdxWildPokemonMove()
        
        # check the velocity of the pokemon
        if self.active_pokemon.getBaseStats().getSpeed() > self.wild_pokemon.getBaseStats().getSpeed():
            self.active_pokemon.useMove(self.active_pokemon.getMoves()[idx_attacker_move].getName(), self.wild_pokemon)
            if self.wild_pokemon.getC_HP() > 0:
                self.wild_pokemon.useMove(self.wild_pokemon.getMoves()[idx_wild_move].getName(), self.active_pokemon)
            else:
                return RESULTS[1]
        else:
            self.wild_pokemon.useMove(self.wild_pokemon.getMoves()[idx_wild_move].getName(), self.active_pokemon)
            if self.active_pokemon.getC_HP() > 0:
                self.active_pokemon.useMove(self.active_pokemon.getMoves()[idx_attacker_move].getName(), self.wild_pokemon)
            else:
                return RESULTS[2]
            
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
            return RESULTS[3]
        else:
            print("You cannot run away")
            return RESULTS[5]
        
    def useItem(self):
        print("What item would you like to use?")
        for i, opt in enumerate(self.trainer.bag.getItems()):
            print(str(i) + ": " + opt.getName())
            
        choice = int(input("Item choice: "))
        item = self.trainer.bag.getItems()[choice]
        
        if item.getName() == "Potion": #TODO generalize to who
            item.use(self.active_pokemon)
        elif item.getName() == "Poké Ball":
            res = item.use(self.wild_pokemon)
            if res:
                return RESULTS[4]
            
        return RESULTS[5]
    
    def changePokemon(self):
        print("Available pokemon:")
        pokemonFromSquad = self.trainer.getSquad()
        available_pokemon = []
        map_to_squad = []
        
        for i in range(0, len(pokemonFromSquad)):
            if not pokemonFromSquad[i].getName() == self.active_pokemon.getName():
                if pokemonFromSquad[i].getC_HP() > 0:
                    available_pokemon.append(pokemonFromSquad[i])
                    map_to_squad.append(i)
        
        
        for i, opt in enumerate(available_pokemon):
            print(str(i) + ": " + opt.getName())
            
        choice = int(input("Pokemon choice: "))
        
        self.active_pokemon = self.trainer.getSquad()[map_to_squad[choice]]
        
        return RESULTS[5]
            
