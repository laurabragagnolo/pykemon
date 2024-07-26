from Character import Character
from Trainer import Trainer
import Pokedex
import MN
import random
from Bag import Bag
from Items import Potion, Pokeball
from PokemonCenter import PokemonCenter
from PokemonStore import PokemonStore
from Battle import Battle
import copy
from Story import Story

def main():
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
    starter = Pokedex.pokedex[choice]
    trainer.addPokemon(copy.deepcopy(starter))
    
    # add potions and pokeballs
    for i in range(0, 10):
        trainer.bag.addItem(Potion("Potion", 20))
        trainer.bag.addItem(Pokeball("Poké Ball"))
    
    print(trainer.toString())
    
    # start the story
    story = Story(trainer)
    story.askWhatDo()
    
    
    
main()