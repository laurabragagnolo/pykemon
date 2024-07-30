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

def main():
    
    print('loading moves...')
    MN = dict()
    with open('/home/paolo/Scrivania/corsi/pykemon/assignment_3/moves.json') as json_file:
        for lin in json_file:
            m = json.loads(lin)
            if not m['power'] == None:
                MN[m['name']] = Move(m['name'], m['type'], m['category'], m['power'], m['accuracy'], m['pp'])
     
    print('loading effectiveness...')
    type_effectiveness = dict()
    i = 0
    with open('/home/paolo/Scrivania/corsi/pykemon/assignment_3/type_effectiveness.json') as json_file:
        for line in json_file:
            t = json.loads(line)
            type_effectiveness[i] = Type_effectiveness(t['attack'], t['defend'], t['effectiveness'])
            i = i + 1
                         
    print('Loading pokedex...')
    pokedex = dict()
    with open('/home/paolo/Scrivania/corsi/pykemon/assignment_3/pokemons.json') as json_file:
        for line in json_file:
            p = json.loads(line)
            pokedex[p['national_pokedex_number']] = Character(p['name'], p['types'], p['baseStats'], [])
            
                
    # Ask to the user to create his pokemon trainer
    input_name = input("What is your name? ")
    trainer = Trainer(input_name)
    
    ## choose the initial pokemon
    while True:
        print('Choose the starter pokemon: ')
        options = ['bulbasaur', 'charmander', 'squirtle']
        options_id = [1, 4, 7]
        for i,opt in zip(options_id, options):
            print(str(i) + '. ' + opt)

        choice = int(input('Pokemon choice: '))

        if choice not in options_id:
            print('Invalid option')
        else:
            break
    
    # add the pokemon to the trainer
    starter = copy.deepcopy(pokedex[choice])
    # take only the move with normal type and the type of the pokemon
    chooseRandomMoves(starter, MN)
    trainer.addPokemon(starter)
    
    # add potions and pokeballs
    for i in range(0, 10):
        trainer.bag.addItem(Potion("Potion", 20))
        trainer.bag.addItem(Pokeball("Poké Ball"))
    
    print(trainer)
    
    # start the story
    story = Story(trainer, pokedex, MN, type_effectiveness)
    story.askWhatDo()
    
    


    
main()
