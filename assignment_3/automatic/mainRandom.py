from Character import Character
from Trainer import Trainer
from Move import Move
import random
from Bag import Bag
from Items import Potion, Pokeball
from PokemonCenter import PokemonCenter
from PokemonStore import PokemonStore
from Battle import Battle
import copy
from Story import Story
import json
from Type_effectiveness import Type_effectiveness
from utils import *
import pickle
import os
    
def main():
    
    print('loading moves...')
    MN = dict()
    with open('/home/paolo/Scrivania/corsi/pykemon/assignment_3/automatic/moves.json') as json_file:
        for lin in json_file:
            m = json.loads(lin)
            if not m['power'] == None:
                MN[m['name']] = Move(m['name'], m['type'], m['category'], m['power'], m['accuracy'], m['pp'])
     
    print('loading effectiveness...')
    type_effectiveness = dict()
    i = 0
    with open('/home/paolo/Scrivania/corsi/pykemon/assignment_3/automatic/type_effectiveness.json') as json_file:
        for line in json_file:
            t = json.loads(line)
            type_effectiveness[i] = Type_effectiveness(t['attack'], t['defend'], t['effectiveness'])
            i = i + 1
                         
    print('Loading pokedex...')
    pokedex = dict()
    with open('/home/paolo/Scrivania/corsi/pykemon/assignment_3/automatic/pokemons.json') as json_file:
        for line in json_file:
            p = json.loads(line)
            pokedex[p['national_pokedex_number']] = Character(p['name'], p['types'], p['baseStats'], [])
            
                
    # Ask to the user to create his pokemon trainer
    #input_name = input("What is your name? ")
    input_name = 'Paolo'
    trainer = Trainer(input_name)
    
    ## choose the initial pokemon
#    while True:
#        print('Choose the starter pokemon: ')
#        options = ['bulbasaur', 'charmander', 'squirtle']
#        options_id = [1, 2, 3]
#        id_pokemons = [1, 4, 7]
#        for i,opt in zip(options_id, options):
#            print(str(i) + '. ' + opt)
#
#        choice = int(input('Pokemon choice: '))
#        choice = id_pokemons[choice-1]
#
#        if choice not in options_id:
#            print('Invalid option')
#        else:
#            break

#     # add potions and pokeballs
#        for i in range(0, 10):
#            trainer.bag.addItem(Potion("Potion", 20))
#            trainer.bag.addItem(Pokeball("Poké Ball"))
#
#        print(trainer)

    id_pokemons = [1, 4, 7, 25]
    n_games = 500
    n_battle = 150
    for choice in id_pokemons:
        all_to_save = []
        for i in range(0, n_games):

            # add the pokemon to the trainer
            starter = copy.deepcopy(pokedex[choice])
            starterMoves(starter, MN)
            trainer = Trainer(input_name)
            trainer.addPokemon(starter)

            # start the story
            story = Story(trainer, pokedex, MN, type_effectiveness)
            to_save = story.automaticExploration(n_battle)
            all_to_save.append(to_save)
            
        c_dir = os.getcwd()
        save_file = c_dir + "/pokemon_" + starter.getName() + ".pickle"
        pickle_out = open(save_file, "wb")
        pickle.dump(all_to_save, pickle_out)
        pickle_out.close()
    
main()