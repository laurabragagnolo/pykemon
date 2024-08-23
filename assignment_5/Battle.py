from Character import Character
from Items import Potion, Pokeball
import random
from utils import *

import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score

RESULTS = {1 : "Your pokemon wins", 2 : "Wild pokemon wins", 3 : "Trainer run away", 4 : "Wild pokemon caught", 5 : "Battle continues", 6 : "Go back"}

class Battle:
    def __init__(self, trainer_pokemon, wild_pokemon, type_effectiveness):
        self.type_effectiveness = type_effectiveness
        self.trainer_pokemon = trainer_pokemon    
        self.wild_pokemon = wild_pokemon
        self.result = 0

        print(len(self.trainer_pokemon))
        self.current_hps = []   
        self.selected_attacks = []
        self.damage_done = []
        
        
    def runBattle(self):
        # start with the choice of the trainer
        res = RESULTS[5]
        count = 0
        while res == RESULTS[5] or res == RESULTS[6]:
            # if res == RESULTS[5]:
            #     print(self.trainer_pokemon.getName() + " HP: " + str(self.trainer_pokemon.getC_HP()))
            #     print(self.wild_pokemon.getName() + " HP: " + str(self.wild_pokemon.getC_HP()))
            
            # always fight
            res = self.fight()
            count = count + 1
        
        if res == RESULTS[1]:
            result_fight = "starter_win"
            self.result = 1
            self.wild_pokemon.setC_HP(0.0)
        else:
            result_fight = "starter_lose"
            self.trainer_pokemon.setC_HP(0.0)

        trainer_pokemon_types = self.trainer_pokemon.getType() 
        wild_pokemon_types = self.wild_pokemon.getType()       
        trainer_pokemon_stats = self.trainer_pokemon.getActStats()  
        wild_pokemon_stats = self.wild_pokemon.getActStats()        

        rows = []
        for t_type in trainer_pokemon_types:
            # map the types of the pokemon into numbers 
            enc_t_type = encode_type(t_type)
            for w_type in wild_pokemon_types:
                enc_w_type = encode_type(w_type)
                row = {
                    "trainer_pokemon_type": enc_t_type,
                    "wild_pokemon_type": enc_w_type,
                    "trainer_hp": trainer_pokemon_stats.getHP(),
                    "trainer_attack": trainer_pokemon_stats.getAttack(),
                    "trainer_defense": trainer_pokemon_stats.getDefense(),
                    "wild_hp": wild_pokemon_stats.getHP(),
                    "wild_attack": wild_pokemon_stats.getAttack(),
                    "wild_defense": wild_pokemon_stats.getDefense(),
                    "result": self.result
                }
                rows.append(row)
        
        # Convert to pandas DataFrame
        df = pd.DataFrame(rows)
        
        return df
   
            
    def fight(self, pokemon=None):
        # take the random move for both pokemon
        if pokemon is None:
            pokemon = self.trainer_pokemon
           
        [idx_move_w, move_type_w] = self.getIdxPokemonMove(self.wild_pokemon)
        all_moves = pokemon.getMoves()
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
        
        idx_move_t = map_to_moves[choice]
        move_type_t = all_moves[idx_move_t].getType()

        self.current_hps.append(pokemon.getC_HP())
        self.selected_attacks.append(move_type_t)

        effect_t = computeEffectiveness(move_type_t, self.wild_pokemon.getType(), self.type_effectiveness)
        effect_w = computeEffectiveness(move_type_w, pokemon.getType(), self.type_effectiveness)
        
        # check the velocity of the pokemon
        if pokemon.getActStats().getSpeed() > self.wild_pokemon.getActStats().getSpeed():
            print("here")
            damage = pokemon.useMove(idx_move_t, self.wild_pokemon, effect_t, False)
            print(damage)
            if self.wild_pokemon.getC_HP() > 0:
                self.wild_pokemon.useMove(idx_move_w, pokemon, effect_w, False)
            else:
                return RESULTS[1]
        else:
            print("there")
            self.wild_pokemon.useMove(idx_move_w, pokemon, effect_w, False)
            if pokemon.getC_HP() > 0:
                damage = pokemon.useMove(idx_move_t, self.wild_pokemon, effect_t, False)
            else:
                return RESULTS[2]
            
        self.damage_done.append(damage)
            
        if pokemon.getC_HP() <= 0:
            return RESULTS[2]
        elif self.wild_pokemon.getC_HP() <= 0:
            return RESULTS[1]
            
        return RESULTS[5]
    
    def getIdxPokemonMove(self, pokemon):
        all_moves = pokemon.getMoves()
        
        idx_move = random.randint(0, len(all_moves) - 1)
        
        return [idx_move, all_moves[idx_move].getType()]


    def runBattle_ml(self):
        res = RESULTS[5]
        count = 0
        while res == RESULTS[5] or res == RESULTS[6]:
            
            # ask to the model if the trainer should run away or fight
            win_probs = []
            for pokemon in self.trainer_pokemon:
                trainer_pokemon_types = pokemon.getType() 
                wild_pokemon_types = self.wild_pokemon.getType()       
                trainer_pokemon_stats = pokemon.getActStats()  
                wild_pokemon_stats = self.wild_pokemon.getActStats()        

                rows = []
                for t_type in trainer_pokemon_types:
                    enc_t_type = encode_type(t_type)
                    for w_type in wild_pokemon_types:
                        enc_w_type = encode_type(w_type)
                        row = {
                            "trainer_pokemon_type": enc_t_type,
                            "wild_pokemon_type": enc_w_type,
                            "trainer_hp": trainer_pokemon_stats.getHP(),
                            "trainer_attack": trainer_pokemon_stats.getAttack(),
                            "trainer_defense": trainer_pokemon_stats.getDefense(),
                            "wild_hp": wild_pokemon_stats.getHP(),
                            "wild_attack": wild_pokemon_stats.getAttack(),
                            "wild_defense": wild_pokemon_stats.getDefense(),
                            "result": self.result
                        }
                        rows.append(row)
                
                # Convert to pandas DataFrame
                df = pd.DataFrame(rows)
                # process data

                stats_data = df

                X = np.hstack([stats_data.values])
                model = joblib.load('model.pkl')
                res = model.predict(X)
                
                # probability of winning for this pokemon
                prob = model.predict_proba(X)
                avg_prob = np.mean(prob, axis=0)
                win_probs.append(avg_prob[1])
            
            # get the pokemon with the highest probability of winning
            max_prob = max(win_probs)
            max_prob_pokemon = win_probs.index(max_prob)
            if max_prob > 0.5:
                # if the probability of winning is greater than 0.5, the trainer should fight
                print(f"You have {max_prob} probability of winning this fight using {self.trainer_pokemon[max_prob_pokemon].getName()} :D!")
                res = RESULTS[5]
            else:
                print("You have no chance! You should run away!")
                # if the probability of winning is less than 0.5, the trainer should run away
                res = RESULTS[3]

            res = self.turn(self.trainer_pokemon[max_prob_pokemon])
                
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
                else:
                    print("Choose another pokemon to continue the battle")
                    for i, opt in enumerate(available_pokemon):
                        print(str(i) + ": " + opt.getName())
                    choice = int(input("Pokemon choice: "))
                    self.active_pokemon = self.trainer.getSquad().getPokemons()[map_to_squad[choice]]
                    res = RESULTS[5]
            elif res == RESULTS[4]: # pokemon caught
                print("You caught the wild pokemon")
            elif res == RESULTS[1]:
                print("You defeated the wild pokemon")
        

        df_results = pd.DataFrame({
            'result': [res]
        })

        return df_results
    
    
    def turn(self, pokemon=None):
        print("What would you like to do?")
        print("1: Fight\n2: Change pokemon\n3: Use item\n4: Run")
        action = int(input("Action selected: "))
        while True:
            if action == 1:
                if pokemon is None:
                    res = self.fight()
                else:
                    res = self.fight(pokemon)
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
                # res = self.escape()
                # if res == RESULTS[5]:
                #     idx_wild_move = self.getIdxWildPokemonMove()
                #     self.wild_pokemon.useMove(idx_wild_move, self.active_pokemon)
                #     if self.active_pokemon.getC_HP() <= 0:
                res = RESULTS[3]
                return res
            else:
                print("Invalid action")
                action = int(input("Action selected: "))

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
            
