import random

class Ant:
    def __init__(self, colony):
        self.colony = colony
        self.health = 100

    def attack(self):
        # Choose a target colony, with a bias towards larger colonies
        if len([c for c in self.colony.game.colonies if c != self.colony and len(c.population) > 0]) > 0:
            if random.random() < 0.7:
                target_colony = max([c for c in self.colony.game.colonies if c != self.colony and not self.colony.is_allied_with(c)], 
                            key=lambda c: (len(c.population), c.resources), default=None)
            else:
                target_colony = random.choice([c for c in self.colony.game.colonies if c != self.colony and not self.colony.is_allied_with(c)])
            if target_colony is not None and len(target_colony.population) > 0:
                target_ant = random.choice(target_colony.population)
                damage = random.randint(5, 10)  
                target_ant.health -= damage
                if target_ant.health <= 0:
                    target_colony.population.remove(target_ant)
                    target_colony.attacked_by_this_turn.append(self.colony)
    
    def gather_resources(self):
        gathered_resources = min(10, self.colony.game.total_resources)
        if random.random() < 0.5 and self.colony.game.total_resources >= gathered_resources:  # 50% chance to gather resources
            self.colony.resources += gathered_resources
            self.colony.game.total_resources -= gathered_resources  # deplete total resources

class WorkerAnt(Ant):
    def gather_resources(self):
        gathered_resources = 20
        if random.random() < 0.7 and self.colony.game.total_resources >= gathered_resources:  # 70% chance to gather resources
            self.colony.resources += gathered_resources
            self.colony.game.total_resources -= gathered_resources  # deplete total resources

class SoldierAnt(Ant):
    def __init__(self, colony):
        super().__init__(colony)
        self.health = 150  # Soldier ants have more health

    def attack(self):
        # Choose a target colony, with a bias towards larger colonies
        if len([c for c in self.colony.game.colonies if c != self.colony and len(c.population) > 0]) > 0:
            if random.random() < 0.7:
                target_colony = max([c for c in self.colony.game.colonies if c != self.colony and not self.colony.is_allied_with(c)], 
                            key=lambda c: (len(c.population), c.resources), default=None)
            else:
                target_colony = random.choice([c for c in self.colony.game.colonies if c != self.colony and not self.colony.is_allied_with(c)])
            if target_colony is not None and len(target_colony.population) > 0:
                target_ant = random.choice(target_colony.population)
                damage = random.randint(20, 40)  
                target_ant.health -= damage
                if target_ant.health <= 0:
                    target_colony.population.remove(target_ant)
                    target_colony.attacked_by_this_turn.append(self.colony)
                    if target_colony.resources > 0:
                        max_gain = 50  # Set a maximum limit to the resources gained
                        gained_resources = min(max_gain, min(3, target_colony.resources))
                        if target_colony.resources >= gained_resources:
                            self.colony.resources += gained_resources  # gain resources
                            target_colony.resources -= gained_resources
                        else:
                            gained_resources = target_colony.resources
                            self.colony.resources += gained_resources  # gain resources
                            target_colony.resources -= gained_resources
    
    def gather_resources(self):
        pass

class ScoutAnt(Ant):
    def __init__(self, colony):
        super().__init__(colony)

    def attack(self):
        pass
    
    def gather_resources(self):
        gathered_resources = 5 # Scout ants gather less resources
        if random.random() < 0.3 and self.colony.game.total_resources >= gathered_resources:  # 30% chance to gather resources
            self.colony.resources += gathered_resources
            self.colony.game.total_resources -= gathered_resources  # deplete total resources

class CaretakerAnt(Ant):
    def __init__(self, colony):
        super().__init__(colony)
        self.health = 50  # Caretaker ants have less health
    
    def heal(self):
        for ant in self.colony.population:
            if ant.health < 100:
                ant.health += 5
                break

    def attack(self):
        pass

    def gather_resources(self):
        pass