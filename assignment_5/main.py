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

import joblib

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
    # input_name = input("What is your name? ")
    trainer = Trainer('Laura')

    print('Using ML recommending system to play!')
    
    ## choose the initial pokemon
    while True:
        print('Choose the starter pokemon: ')
        id_pokemons = list(pokedex['Pokemon Number'])
        print(id_pokemons)
        choice = int(input('Pokemon choice: '))

        if choice not in id_pokemons:
            print('Invalid option')
        else:
            break
    
    # add the pokemon to the trainer
    starter = copy.deepcopy(pokedex.loc[pokedex['Pokemon Number'] == choice]['Pokemon'].values[0])
    starter.setLevel(random.randint(1, 20))
    # take only the move with normal type and the type of the pokemon
    chooseRandomMoves(starter, MN)
    trainer.addPokemon(starter)
    
    # add potions and pokeballs
    for i in range(0, 10):
        trainer.bag.addItem(Potion("Potion", 20))
        trainer.bag.addItem(Pokeball("Poké Ball"))
    
    print(trainer)
    
    # start the story
    story = Story(trainer, pokedex, MN, type_effectiveness['Type Effectiveness'])
    story.askWhatDo()
    
    
main()
