import random
import time
import random
from abc import ABC, abstractmethod


def generate_colony_name():
    adjectives = {
        "Ancient",
        "Beautiful",
        "Barren",
        "Bustling",
        "Chaotic",
        "Fertile",
        "Fragrant",
        "Humble",
        "Magnificent",
        "Mysterious",
        "Pretty",
        "Raucous",
        "Rich",
        "Savage",
        "Vast",
        "Violent"
    }
    nouns = {
        "Colony",
        "Settlement",
        "Haven",
        "Realm",
        "Territory",
        "Outpost",
        "Domain",
        "Land",
        "Zone",
        "Frontier",
        "Enclave",
        "Sanctuary",
        "Stronghold"
    }
    adjective = random.choice(list(adjectives))
    noun = random.choice(list(nouns))
    return f"{adjective} {noun}"

class Ant(ABC):
    def __init__(self, colony):
        self.colony = colony
        self.health = 100
        self.position = (0, 0)

    @abstractmethod
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
    
    @abstractmethod
    def gather_resources(self):
        gathered_resources = 20
        # 30% chance to gather resources
        if random.random() < 0.3 and self.colony.game.total_resources >= gathered_resources:  
            self.colony.resources += gathered_resources
            # deplete total resources
            self.colony.game.total_resources -= gathered_resources  
            
    def move(self, direction):
        new_position = self.position + direction
        if game.is_valid_position(new_position):
            self.position = new_position

class WorkerAnt(Ant):
    def __init__(self, colony):
        super().__init__(colony)
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
        gathered_resources = 20
        # 30% chance to gather resources
        if random.random() < 0.3 and self.colony.game.total_resources >= gathered_resources:
            self.colony.resources += gathered_resources
            # deplete total resources
            self.colony.game.total_resources -= gathered_resources  
class SoldierAnt(Ant):
    def __init__(self, colony):
        super().__init__(colony)
        self.health = 150  # Soldier ants have more health

    def attack(self):
        # Choose a target colony, with a bias towards larger colonies
        target_colony = self._choose_target_colony()
        if target_colony is not None and len(target_colony.population) > 0:
            target_ant = random.choice(target_colony.population)
            damage = random.randint(20, 40)
            target_ant.health -= damage
            if target_ant.health <= 0:
                target_colony.population.remove(target_ant)
                target_colony.attacked_by_this_turn.append(self.colony)
                self._gain_resources(target_colony)

    def _choose_target_colony(self):
        colonies = [c for c in self.colony.game.colonies if c != self.colony and len(c.population) > 0 and not self.colony.is_allied_with(c)]
        if len(colonies) == 0:
            return None
        if random.random() < 0.7:
            return max(colonies, key=lambda c: (len(c.population), c.resources), default=None)
        else:
            return random.choice(colonies)

    def _gain_resources(self, target_colony):
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
        # This method is intentionally empty, Soldiers does not gather resources this way.
        pass

class ScoutAnt(Ant):
    def __init__(self, colony):
        super().__init__(colony)
        self.health = 80

    def attack(self):
        # Scout ants do not attack
        pass

    def gather_resources(self):
        gathered_resources = 5 # Scout ants gather less resources
        # 70% chance to gather resources
        if random.random() < 0.7 and self.colony.game.total_resources >= gathered_resources:
            self.colony.resources += gathered_resources
            # deplete total resources
            self.colony.game.total_resources -= gathered_resources  

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
        # Caretaker ants do not attack
        pass

    def gather_resources(self):
        # This method is empty because Caretaker ants do not gather resources.
        pass
    
    def position(self):
        # This method is empty because Caretaker ants do not move.
        pass

class Cell:
    def __init__(self):
        self.resources = 0  # The amount of resources in the cell
        self.enemy = None  # The enemy in the cell, if any

    def has_resources(self):
        return self.resources > 0

    def get_resources(self):
        return self.resources

    def deplete_resources(self, amount):
        self.resources = max(0, self.resources - amount)

    def has_enemy(self):
        return self.enemy is not None

    def get_enemy(self):
        return self.enemy

    def set_enemy(self, enemy):
        self.enemy = enemy

class Colony:
    MAX_ALLIES = 3  # Maximum number of allies a colony can have
    def __init__(self, name, game):
        self.name = name
        self.population = []
        self.resources = 1000
        self.game = game
        self.alliances = []
        self.attacked_by_this_turn = []
        self.ANT_CREATION_PROBABILITY = 1

    def is_allied_with(self, other_colony):
        return other_colony in self.alliances

    def form_alliance(self, other_colony):
        if len(self.population) < len(other_colony.population) and not self.is_allied_with(other_colony) and len(self.alliances) < self.MAX_ALLIES:
            self.alliances.append(other_colony)
            other_colony.alliances.append(self)

    def break_alliance(self, other_colony):
        if self.is_allied_with(other_colony):
            self.alliances.remove(other_colony)
            other_colony.alliances.remove(self)

    @property
    def capacity(self):
        return self.resources // 100

    def create_ant(self):
        if len(self.population) < self.capacity and random.random() < self.ANT_CREATION_PROBABILITY:
            ant_type = random.choice([WorkerAnt, SoldierAnt, ScoutAnt, CaretakerAnt])
            base_cost = {WorkerAnt: 10, SoldierAnt: 20, ScoutAnt: 5, CaretakerAnt: 15}[ant_type]
            soldier_ants = len([ant for ant in self.population if isinstance(ant, SoldierAnt)])
            max_ants_to_create = int(self.resources / base_cost) + soldier_ants
            num_ants_to_create = random.randint(1, max_ants_to_create)  # Choose a random number of ants to create
            new_ant_cost = base_cost + soldier_ants * 2

            if self.resources >= new_ant_cost * num_ants_to_create:
                for _ in range(num_ants_to_create):
                    new_ant = ant_type(self)
                    self.population.append(new_ant)
                    self.resources -= new_ant_cost

class Game():
    def __init__(self, num_colonies):  # Add num_colonies as an argument
        self.colonies = [self.create_colony(generate_colony_name()) for _ in range(num_colonies)]
        self.map_width = 10  # Replace with your actual map width
        self.map_height = 10  # Replace with your actual map height
        self.map = [[Cell() for _ in range(self.map_width)] for _ in range(self.map_height)]
        self.MIN_COLONIES_FOR_ALLIANCES = num_colonies // 2  # Minimum number of colonies for alliances to be allowed
        self.ALLIANCE_BREAK_PROBABILITY = 0.20 # 0.05  # 5% chance to break an alliance each turn
        self.RESOURCE_THRESHOLD = 200  # Threshold for resource scarcity
        self.colonies = []
        self.turn = 0
        self.total_resources = 1000 * num_colonies  # new attribute for total resources
        
    def create_colony(self, name):
        new_colony = Colony(name, self)
        new_colony.create_ant() 
        self.colonies.append(new_colony)

    def next_turn(self):
        self.turn += 1
        self.update_resources()
        self.update_alliances()
        self.perform_actions()
        self.remove_empty_colonies()
        self.check_win_condition()
        return len(self.colonies) > 1
    
    def update_resources(self):
        if self.turn % 10 == 0:
            self.total_resources += 1000

    def update_alliances(self):
        for colony in self.colonies:
            colony.attacked_by_this_turn.clear()  # Clear the list at the start of each turn

            self.check_alliance_break(colony)

            if len(self.colonies) == 2:
                self.break_alliances()

            if len(self.colonies) >= self.MIN_COLONIES_FOR_ALLIANCES:
                self.form_alliances(colony)

    def check_alliance_break(self, colony):
        for ally in list(colony.alliances):
            if self.should_break_alliance(colony, ally):
                colony.break_alliance(ally)

    def should_break_alliance(self, colony, ally):
        return random.random() < self.ALLIANCE_BREAK_PROBABILITY or len(colony.population) > 1.2 * len(ally.population) or ally in colony.attacked_by_this_turn or colony.resources < self.RESOURCE_THRESHOLD

    def break_alliances(self):
        for colony in self.colonies:
            colony.break_alliances()

    def form_alliances(self, colony):
        for other_colony in self.colonies:
            if self.should_form_alliance(colony, other_colony):
                colony.form_alliance(other_colony)

    def should_form_alliance(self, colony, other_colony):
        return len(colony.population) < len(other_colony.population) and not colony.is_allied_with(other_colony) and random.random() < 0.2

    def perform_actions(self):
        for colony in self.colonies:
            colony.create_ant()

            # In the game loop
            for ant in colony.population:
                nearby_resources = game.get_nearby_resources(ant.position)
                nearby_enemies = game.get_nearby_enemies(ant.position)
                if isinstance(ant, CaretakerAnt):
                    ant.heal()
                elif nearby_resources:
                    ant.gather_resources(nearby_resources)
                elif nearby_enemies:
                    ant.attack(nearby_enemies)
                else:
                    ant.move(self.random_direction())
                    
    def get_nearby_enemies(self, position):
        nearby_enemies = []
        for direction in [(0, -1), (1, 0), (0, 1), (-1, 0)]:  # Up, right, down, left
            new_position = (position[0] + direction[0], position[1] + direction[1])
            if self.is_valid_position(new_position):
                cell = self.map[new_position[1]][new_position[0]]
                if cell.has_enemy():
                    nearby_enemies.append(cell.get_enemy())
        return nearby_enemies

    def get_nearby_resources(self, position):
        nearby_resources = []
        for direction in [(0, -1), (1, 0), (0, 1), (-1, 0)]:  # Up, right, down, left
            new_position = (position[0] + direction[0], position[1] + direction[1])
            if self.is_valid_position(new_position):
                cell = self.map[new_position[1]][new_position[0]]
                if cell.has_resources():
                    nearby_resources.append(cell.get_resources())
        return nearby_resources
            
    def random_direction(self):
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # Up, right, down, left
        return random.choice(directions)
                    
    def is_valid_position(self, position):
        return 0 <= position[0] < self.map_width and 0 <= position[1] < self.map_height and not self.map[position[1]][position[0]].is_obstacle

    def remove_empty_colonies(self):
        self.colonies = [colony for colony in self.colonies if len(colony.population) > 0]

    def check_win_condition(self):
        return len(self.colonies) == 1

# Initialize game with a number of colonies between 50 and 100
num_colonies = random.randint(20, 40)
game = Game(num_colonies)

while True:
    if not game.next_turn() or game.check_win_condition():
        break
    time.sleep(1)
    print(f"Turn {game.turn}")
    for colony in game.colonies:
        worker_ants = len([ant for ant in colony.population if isinstance(ant, WorkerAnt)])
        soldier_ants = len([ant for ant in colony.population if isinstance(ant, SoldierAnt)])
        scout_ants = len([ant for ant in colony.population if isinstance(ant, ScoutAnt)])
        caretaker_ants = len([ant for ant in colony.population if isinstance(ant, CaretakerAnt)])
        print(f"{colony.name} has {len(colony.population)} ants ("
            f"Worker: {worker_ants:<1}. "
            f"Soldier: {soldier_ants:<1}. "
            f"Scout: {scout_ants:<1}. "
            f"Caretaker: {caretaker_ants:<1}. "
            f"capacity {colony.capacity:<1}. "
            f"and colony resources {colony.resources:<1}. "
            f"total world resources {colony.game.total_resources:<1} resources.")
