import random
import copy

import pandas as pd
import math

def chooseRandomMoves(pokemon, MN):
    types_move = [t for t in pokemon.getType()]
    types_move.append('normal')
    available_moves = []  

    for move in list(MN['Move Name']):
        if MN.loc[MN['Move Name'] == move]['Move'].values[0].getType() in types_move:
            available_moves.append(MN.loc[MN['Move Name'] == move]['Move'].values[0])
    
    how_many_moves = random.randint(1, 4)
    moves = []
    for i in range(0, how_many_moves):
        idx_move = random.choice(range(0, len(available_moves)))
        moves.append(copy.deepcopy(available_moves.pop(idx_move)))
    pokemon.setMoves(moves)
    
def computeEffectiveness(type_attack, type_defend, type_effectiveness):
    effect = 1
    for te in type_effectiveness:
        if te.getAttack() == type_attack and te.getDefend() in type_defend:
            effect = effect * te.getDamageRelations()
    return effect


def starterMoves(starter, MN):
    if starter.getName() == 'bulbasaur':
        starter.setMoves([copy.deepcopy(MN.loc[MN['Move Name'] == 'tackle']['Move'].values[0]), copy.deepcopy(MN.loc[MN['Move Name'] == 'vine whip']['Move'].values[0])])
    elif starter.getName() == 'charmander':
        starter.setMoves([copy.deepcopy(MN.loc[MN['Move Name'] == 'tackle']['Move'].values[0]), copy.deepcopy(MN.loc[MN['Move Name'] == 'ember']['Move'].values[0])])
    elif starter.getName() == 'squirtle':
        starter.setMoves([copy.deepcopy(MN.loc[MN['Move Name'] == 'tackle']['Move'].values[0]), copy.deepcopy(MN.loc[MN['Move Name'] == 'water gun']['Move'].values[0])])
    elif starter.getName() == 'pikachu':
        starter.setMoves([copy.deepcopy(MN.loc[MN['Move Name'] == 'thunder shock']['Move'].values[0]), copy.deepcopy(MN.loc[MN['Move Name'] == 'quick attack']['Move'].values[0])])
    else:
        # for the other pokemons, we choose randomly the moves, based on the type of the pokemon
        chooseRandomMoves(starter, MN)

TYPES = {
    'normal': 0,
    'fire': 1,
    'water': 2,
    'electric': 3,
    'grass': 4,
    'ice': 5,
    'fighting': 6,
    'poison': 7,
    'ground': 8,
    'flying': 9,
    'psychic': 10,
    'bug': 11,
    'rock': 12,
    'ghost': 13,
    'dragon': 14,
    'dark': 15,
    'steel': 16,
    'fairy': 17
}

def encode_type(type_name):
    return TYPES[type_name]