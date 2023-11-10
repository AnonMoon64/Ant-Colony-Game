import random

class Colony:
    MAX_ALLIES = 3  # Maximum number of allies a colony can have
    def __init__(self, name, game):
        self.name = name
        self.population = []
        self.resources = 1000
        self.game = game
        self.alliances = []
        self.attacked_by_this_turn = []  # New attribute to track attacks
        self.ANT_CREATION_PROBABILITY = 0.9

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