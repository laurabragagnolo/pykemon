from Move import Move
from BaseStats import BaseStats
import random
import math
    
class Character:
    def __init__(self, name, type_, baseStats, moves = [], level = 1):
        self.name = name
        self.level = level
        self.type = type_
        self.baseStats = baseStats
        # check no repetition in the moves
        c_moves = []
        if len(moves) > 0:
            c_moves.append(moves[0])
            for i in range(1, len(moves)):
                repeated = False
                for j in range(1, len(c_moves)):
                    if c_moves[j].getName() == moves[i].getName():
                        repeated = True
                        break
                        #print("You cannot have the same move twice.")
                if repeated == False:
                    c_moves.append(moves[i])    
                    
        self.moves = c_moves
        self.c_hp = baseStats.hp
      
    def useMove(self, name_move, opponent_pokemon):
        move = self.moves[name_move]
        if random.random() < move.getAccuracy():
            stability = 1
            if move.getType() in self.type:
                stability = 1.5
            effect = 1
            critical= 1
            if random.random() < self.baseStats.getSpeed()/512:
                critical = 2
            luck = random.uniform(0.85, 1)
            modifier = stability * effect * critical * luck
            damage = math.floor(((2*self.level + 10)/250) * (self.baseStats.getAttack()/opponent_pokemon.baseStats.getDefense()) * move.getPower() + 2)*modifier
            opponent_pokemon.hitted(damage)
        else:
            print(self.name + ' tried to use ' + move.getName() + ' but he missed the target')
            
        move.setPP(move.getPP() - 1)
    
    def getName(self):
        return self.name
    
    def getMoves(self):
        return self.moves
    
    def getBaseStats(self):
        return self.baseStats
    
    def hitted(self, damage):
        self.c_hp -= damage
        if self.c_hp <= 0:
            print(self.name + ' fainted')
            
    def toString(self):
        string = "Name: " + str(self.name) + " Type: " 
        for i in range(0, len(self.type)):
            string += self.type[i] + "-"
        string += " Level: " + str(self.level) + " current HP: " + str(self.c_hp) +"\n             Base Stats: " + self.baseStats.toString() + "\n             Moves: " 
        for i in range(0, len(self.moves)):
            string += "\n          " + self.moves[i].toString()
            
        return string
        
