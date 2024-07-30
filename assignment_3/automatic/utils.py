import random
import copy

def chooseRandomMoves(pokemon, MN):
    types_move = [t for t in pokemon.getType()]
    types_move.append('normal')
    available_moves = []
    for move in list(MN.keys()):
        if MN[move].getType() in types_move:
            available_moves.append(MN[move])
    how_many_moves = random.randint(1, 4)
    moves = []
    for i in range(0, how_many_moves):
        idx_move = random.choice(range(0, len(available_moves)))
        moves.append(copy.deepcopy(available_moves.pop(idx_move)))
    pokemon.setMoves(moves)
    
def computeEffectiveness(type_attack, type_defend, type_effectiveness):
    effect = 1
    for te in type_effectiveness.values():
        if te.getAttack() == type_attack and te.getDefend() in type_defend:
            effect = effect * te.getDamageRelations()
    return effect

def starterMoves(starter, MN):
    if starter.getName() == 'bulbasaur':
        starter.setMoves([copy.deepcopy(MN['tackle']), copy.deepcopy(MN['razor leaf'])])
    elif starter.getName() == 'charmander':
        starter.setMoves([copy.deepcopy(MN['tackle']), copy.deepcopy(MN['ember'])])
    elif starter.getName() == 'squirtle':
        starter.setMoves([copy.deepcopy(MN['tackle']), copy.deepcopy(MN['water gun'])])
    elif starter.getName() == 'pikachu':
        starter.setMoves([copy.deepcopy(MN['thunder shock']), copy.deepcopy(MN['quick attack'])])