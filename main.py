from Character import Character
from Trainer import Trainer
import Pokedex
import MN
import random


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
    trainer.addPokemon(starter)
    print("Trainer:")
    print(trainer.toString())
    
    ## get random an opposite pokemon
    opponent_id = random.choice([1, 4, 7])
    opponent = Pokedex.pokedex[opponent_id]
    print("Opponent:")
    print(opponent.toString())    
    
    ## choose a move to use again the pokemon
    for i, move in enumerate(starter.getMoves()):
        print(str(i) + '. ' + move.getName())
    idx_move = int(input('Choose a move to use: '))
    
    trainer.pokemon[0].useMove(idx_move, opponent)
    
    print(opponent.toString())
    
    
main()