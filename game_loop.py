import time
from ant import *
from colony import *
from game import *

# Initialize game with a number of colonies between 2 and 100
num_colonies = 50 # random.randint(2, 100)
game = Game(num_colonies)

while True:
    if not game.next_turn():
        break
    time.sleep(0.1)
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