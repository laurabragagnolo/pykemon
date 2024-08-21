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

import pandas as pd
import tqdm
    
def main():
    
    print('loading moves...')
    moves_list = []
    moves_names_list = []
    with open('moves.json') as json_file:
        for lin in json_file:
            m = json.loads(lin)
            if not m['power'] == None:
                moves_names_list.append(m['name'])
                moves_list.append(Move(m['name'], m['type'], m['category'], m['power'], m['accuracy'], m['pp']))

    MN = pd.DataFrame({
        'Move Name': moves_names_list,
        'Move': moves_list
    })
     
    print('loading effectiveness...')
    type_effectiveness_list = []
    with open('type_effectiveness.json') as json_file:
        for line in json_file:
            t = json.loads(line)
            type_effectiveness_list.append(Type_effectiveness(t['attack'], t['defend'], t['effectiveness']))
    
    type_effectiveness = pd.DataFrame({
        'Type Effectiveness': type_effectiveness_list
    })
                         
    print('Loading pokedex...')
    pokedex_list = []
    pokedex_numbers_list = []
    with open('pokemons.json') as json_file:
        for line in json_file:
            p = json.loads(line)
            pokedex_numbers_list.append(p['national_pokedex_number'])
            pokedex_list.append(Character(p['name'], p['types'], p['baseStats'], []))

    pokedex = pd.DataFrame({
        'Pokemon Number': pokedex_numbers_list,
        'Pokemon': pokedex_list
    })
                
    # Ask to the user to create his pokemon trainer
    #input_name = input("What is your name? ")
    input_name = 'Lau'
    trainer = Trainer(input_name)

    id_pokemons = [1, 4, 7, 25]
    random_index = random.choice(id_pokemons)
    starter = copy.deepcopy(pokedex.loc[pokedex['Pokemon Number'] == random_index]['Pokemon'].values[0])
    starter.setLevel(random.randint(1, 20))
    print("Starter: ", starter.getName())
    print("Level: ", starter.getLevel())
    n_games = 10
    n_battle = 150

    all_to_save = []
    for i in tqdm.tqdm(range(0, n_games)):
        starterMoves(starter, MN)
        trainer = Trainer(input_name)
        trainer.addPokemon(starter)

        # start the story
        story = Story(trainer, pokedex, MN, type_effectiveness['Type Effectiveness'])
        
        to_save = story.automaticExploration(n_battle)
        all_to_save.append(to_save)

    df = pd.DataFrame(all_to_save)
            
    c_dir = os.getcwd()
    save_file = c_dir + "/pokemon_" + starter.getName() + ".csv"
    df.to_csv(save_file, index=False)
    
main()