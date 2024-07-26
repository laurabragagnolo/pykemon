
from Character import Character
from BaseStats import BaseStats
from MN import MN
import copy

pokedex ={
    1 : Character('bulbasaur', ['grass', 'poison'], BaseStats(45, 49, 49, 45, 65), [copy.deepcopy(MN['tackle']), copy.deepcopy(MN['razor leaf'])]),
    4 : Character('charmander', ['fire'], BaseStats(39, 52, 43, 65, 50), [copy.deepcopy(MN['tackle']), copy.deepcopy(MN['ember'])]),
    7 : Character('squirtle', ['water'], BaseStats(44, 48, 65, 43, 50), [copy.deepcopy(MN['tackle']), copy.deepcopy(MN['water gun'])]),
    10: Character('caterpie', ['bug'], BaseStats(45, 30, 35, 45, 20), [copy.deepcopy(MN['twineedle'])]),
    16: Character('pidgey', ['normal', 'flying'], BaseStats(40, 45, 40, 56, 35), [copy.deepcopy(MN['tackle']), copy.deepcopy(MN['peack'])]),
    19: Character('rattata', ['normal'], BaseStats(30, 56, 35, 72, 25), [copy.deepcopy(MN['tackle'])]),
}
