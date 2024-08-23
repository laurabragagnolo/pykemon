from Move import Move
from BaseStats import BaseStats
import random
import math

DEFAULT_MOVE = Move("Struggle", "normal", "physical", 50, 1.0, float('inf'))
    
class Character:
    def __init__(self, name, type_, baseStats, moves = [], level = 1):
        self.name = name
        self.level = level
        self.type = type_
        self.baseStats = BaseStats(baseStats['hp'], baseStats['attack'], baseStats['defense'], baseStats['speed'], baseStats['special'])
        self.actStats = self.computeActStats(self.baseStats, level)

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
        self.c_hp = self.actStats.getHP()
    
    def computeActStats(self, baseStats, level):
        actStats = BaseStats()
        actStats.setHP(math.floor(((baseStats.getHP() * 2 * level / 100) + level + 10)))
        actStats.setAttack(math.floor(((baseStats.getAttack() * 2 * level / 100) + 5)))
        actStats.setDefense(math.floor(((baseStats.getDefense() * 2 * level / 100) + 5)))
        actStats.setSpeed(math.floor(((baseStats.getSpeed() * 2 * level / 100) + 5)))
        actStats.setSpecial(math.floor(((baseStats.getSpecial() * 2 * level / 100) + 5)))
        
        return actStats
      
    def useMove(self, idx_move, opponent_pokemon, effect, considerPP = True):
        if idx_move == -1:
            move = DEFAULT_MOVE
        else:
            move = self.moves[idx_move]
        if move.getAccuracy() is None or random.random() < move.getAccuracy():
            stability = 1
            if move.getType() in self.type:
                stability = 1.5
            critical= 1
            if random.random() < self.actStats.getSpeed()/512:
                critical = 2
            luck = random.uniform(0.85, 1)
            modifier = stability * effect * critical * luck
            damage = math.floor(((2*self.level + 10)/250) * (self.actStats.getAttack()/opponent_pokemon.actStats.getDefense()) * move.getPower() + 2)*modifier
            opponent_pokemon.hitted(damage)
            # print(self.name + ' used ' + move.getName())
        else:
            # print(self.name + ' tried to use ' + move.getName() + ' but he missed the target')
            damage = 0
           
        if considerPP: 
            move.setPP(move.getPP() - 1)

        return damage
    
    def getName(self):
        return self.name
    
    def getType(self):
        return self.type
    
    def getMoves(self):
        return self.moves
    
    def getBaseStats(self):
        return self.baseStats
         
    def getActStats(self):
        return self.actStats
    
    def getC_HP(self):
        return self.c_hp
    
    def restoreC_HP(self):
        self.c_hp = self.actStats.getHP()
        
    def restorePP(self):
        for i in range(0, len(self.moves)):
            self.moves[i].setPP(self.moves[i].getMaxPP())
    
    def restoreMovesPP(self):
        for i in range(0, len(self.moves)):
            self.moves[i].setPP(self.moves[i].getMaxPP())
    
    def addC_HP(self, add_hp):
        self.c_hp = self.c_hp + add_hp
        
    def setC_HP(self, value):
        self.c_hp = value

    def setLevel(self, level):
        self.level = level
        self.actStats = self.computeActStats(self.baseStats, level)

    def getLevel(self):
        return self.level
        
    def setMoves(self, moves):
        c_moves = []
        if len(moves) > 0:
            c_moves.append(moves[0])
            for i in range(1, len(moves)):
                repeated = False
                for j in range(1, len(c_moves)):
                    if c_moves[j].getName() == moves[i].getName():
                        repeated = True
                        break
                        # print("You cannot have the same move twice.")
                if repeated == False:
                    c_moves.append(moves[i])    
                    
        self.moves = c_moves
    
    def hitted(self, damage):
        self.c_hp -= damage
        # if self.c_hp <= 0:
            # print(self.name + ' dead')
            
    def __str__(self):
        string = "Name: " + str(self.name) + " Type: " 
        for i in range(0, len(self.type)):
            string += self.type[i] + "-"
        string += " Level: " + str(self.level) + " current HP: " + str(self.c_hp) +"\n             Act Stats: " + str(self.actStats) + "\n             Moves: " 
        for i in range(0, len(self.moves)):
            string += "\n          " + str(self.moves[i])
            
        return string
    
    def __repr__(self):
        string = "Name: " + str(self.name) + " Type: " 
        for i in range(0, len(self.type)):
            string += self.type[i] + "-"
        string = string[:-1]
        string += " Level: " + str(self.level) + " current HP: " + str(self.c_hp) +"\n             Act Stats: " + str(self.actStats) + "\n             Moves: " 
        for i in range(0, len(self.moves)):
            string += "\n          " + str(self.moves[i])
                        
        return string
        
