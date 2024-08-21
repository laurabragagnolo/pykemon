class Type_effectiveness:
    def __init__(self, attack, defend, damage_relations):
        self.damage_relations = damage_relations
        self.attack = attack
        self.defend = defend
        
    def getDamageRelations(self):
        return self.damage_relations
    
    def getAttack(self):
        return self.attack
    
    def getDefend(self):
        return self.defend